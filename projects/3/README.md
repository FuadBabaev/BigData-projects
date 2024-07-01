# Finding the Shortest Path in a Graph

## Overview

This project implements an algorithm to find the shortest path in a graph using the Breadth-first search (BFS) algorithm. The dataset used is a snapshot of the Twitter social network graph.

## Data

The dataset is available in two parts:
- `/datasets/twitter/twitter_sample_small.tsv` (660 KB, 54485 edges, 54161 vertices)
- `/datasets/twitter/twitter.tsv` (64 MB, 5432909 edges, 100000 vertices)

## Task

The goal is to find the shortest path between two specified vertices in the graph. The implementation should handle cycles and include a stopping mechanism upon reaching `max_path_length`.

## Implementation

The solution is implemented in `shortest_path.py` using Spark. The program takes four parameters:
1. Start node
2. End node
3. Path to the dataset
4. Path to the output directory

## Running the Program

To run the program, use the following command:

```sh
PYSPARK_PYTHON=/opt/conda/envs/dsenv/bin/python spark3-submit \
    --master yarn \
    --name checker \
    projects/3/shortest_path.py 12 34 /datasets/twitter/twitter.tsv hw3_output
```
