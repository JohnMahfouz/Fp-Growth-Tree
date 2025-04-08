# FP-Growth Algorithm for Frequent Itemset Mining

## Overview

This repository contains an implementation of the **FP-Growth** algorithm for mining frequent itemsets from transaction data. The algorithm reads transaction data from an Excel file, constructs an FP-tree, and then identifies frequent itemsets (from 2-itemsets to 5-itemsets). It further generates strong association rules based on metrics like **confidence** and **lift**.

## Features

- **FP-Growth Algorithm**: Efficiently constructs a compact FP-tree for mining frequent itemsets.
- **Frequent Itemsets Generation**: Mines itemsets of varying sizes (2-itemsets, 3-itemsets, 4-itemsets, 5-itemsets).
- **Association Rules**: Generates strong association rules based on minimum confidence.
- **Lift Calculation**: Computes lift values for evaluating the strength of the association between itemsets.
