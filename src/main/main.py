# src/main/main.py

import sys
from src.main.infrastructure.spark_config import create_spark_session, stop_spark_session
from src.main.infrastructure.data_loader import load_dataset_from_spmf
from src.main.core.twu_filter import calculate_global_twu, filter_and_sort_items
from src.main.core.utility_list_builder import build_utility_lists_parallèlement
from src.main.core.hui_miner import hui_miner_dfs

def run_distributed_huim(file_path: str, min_util: float):
    """
    Coordinates the entire distributed HUIM pipeline using Spark and local DFS mining.
    """
    # 1. Initialize Spark Context via Infrastructure
    spark = create_spark_session("Distributed_HUIM_Main_Execution")
    
    try:
        print(f"[INFO] Loading dataset from: {file_path}")
        transactions_rdd = load_dataset_from_spmf(spark, file_path)
        transactions_rdd.cache() # Cache RDD to optimize dual-pass processing
        
        # 2. First Pass: Compute global TWU and perform Pruning
        print("[INFO] Phase 1: Computing Global TWU MapReduce...")
        twu_map = calculate_global_twu(transactions_rdd)
        
        print(f"[INFO] Phase 1: Filtering and sorting items with min_util={min_util}...")
        sorted_promising_items = filter_and_sort_items(twu_map, min_util)
        print(f"[INFO] Promising items sorted: {sorted_promising_items}")
        
        if not sorted_promising_items:
            print("[WARN] No promising items found above the threshold. Exiting.")
            return {}

        # 3. Second Pass: Build Distributed Utility-Lists
        print("[INFO] Phase 2: Building Distributed Utility-Lists...")
        utility_lists_map = build_utility_lists_parallèlement(transactions_rdd, sorted_promising_items)
        
        # 4. Phase 3: Local DFS Mining (Zero-Network Communication)
        print("[INFO] Phase 3: Launching Local HUIM DFS Mining...")
        extensions = [(item, utility_lists_map[item]) for item in sorted_promising_items if item in utility_lists_map]
        
        high_utility_itemsets = {}
        hui_miner_dfs(
            prefix_items=[],
            prefix_ul=None,
            extensions=extensions,
            min_util=min_util,
            high_utility_itemsets=high_utility_itemsets
        )
        
        # 5. Output results
        print("\n=========================================")
        print(f"🎉 SUCCESS: Extracted {len(high_utility_itemsets)} High-Utility Itemsets (HUIs)")
        print("=========================================")
        for itemset, utility in high_utility_itemsets.items():
            print(f"Itemset: {list(itemset)} ---> Utility: {utility}")
        print("=========================================\n")
        
        return high_utility_itemsets

    finally:
        # Guarantee resources release
        stop_spark_session(spark)


if __name__ == "__main__":
    # Default execution values if no CLI arguments provided
    dataset_path = "src/tests/infrastructure/sample.txt" if len(sys.argv) < 2 else sys.argv[1]
    threshold = 45.0 if len(sys.argv) < 3 else float(sys.argv[2])
    
    run_distributed_huim(dataset_path, threshold)