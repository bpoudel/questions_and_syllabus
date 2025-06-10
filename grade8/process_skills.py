import json
import random
import os
import re

# Example questions for each skill
example_questions = {
    "AA1": [
        "Is √2 a rational or irrational number? Explain your reasoning.",
        "Classify each number as rational or irrational: π, 3.14, 0.333..., √9",
        "Create a Venn diagram to sort these numbers: 1.5, √3, 22/7, 3.141592..."
    ],
    "AA2": [
        "Write 3/8 as a decimal. Is it terminating or repeating?",
        "Explain why 2/5 results in a terminating decimal.",
        "Convert 7/6 to a decimal and identify its decimal pattern."
    ],
    "AA3": [
        "Convert 2/3 to a repeating decimal.",
        "What is 5/11 as a repeating decimal?",
        "Write 1/7 as a repeating decimal and identify the repeating part."
    ],
    "AA4": [
        "Convert 0.333... to a fraction.",
        "Write 0.583333... as a fraction in simplest form.",
        "Express 2.456456456... as a fraction."
    ],
    "AB1": [
        "Find two consecutive integers between which √17 lies.",
        "Approximate √30 to the nearest tenth.",
        "Without a calculator, estimate √50 and explain your reasoning."
    ],
    "AB2": [
        "Find two consecutive integers between which ∛20 lies.",
        "Approximate ∛100 to the nearest whole number.",
        "Estimate ∛75 and explain your method."
    ],
    "AB3": [
        "Place √2, √3, and √4 on a number line.",
        "Mark the position of π on a number line between 3 and 4.",
        "Locate √10 on a number line and explain how you determined its position."
    ],
    "AB4": [
        "Compare √8 and 3 without using a calculator.",
        "Order from least to greatest: √5, 2.5, π",
        "Which is larger, √20 or 4.5? Justify your answer."
    ],
    "AB5": [
        "Use a calculator to compare √11 and √12.",
        "Order from least to greatest: √50, 7.1, √49",
        "Find three irrational numbers between 3 and 4 using a calculator."
    ],
    "AB6": [
        "Estimate the value of √7 + √3.",
        "Without a calculator, estimate π × √2.",
        "Approximate the sum: √5 + √20"
    ]
}

# Khan Academy URL mappings
khan_academy_urls = {
    # Number System - Additional Links
    "AA1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-irrational-numbers/v/rational-and-irrational-numbers",
    "AA2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-repeating-decimals/v/converting-repeating-decimals-to-fractions-1",
    "AA3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-repeating-decimals/v/converting-fractions-to-repeating-decimals",
    "AA4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-repeating-decimals/v/converting-repeating-decimals-to-fractions-1",
    "AB1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-roots/v/approximating-square-roots",
    "AB2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-roots/v/approximating-cube-roots",
    "AB3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-irrational-numbers/v/plotting-irrational-numbers",
    "AB4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-irrational-numbers/v/comparing-irrational-numbers",
    "AB5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-irrational-numbers/v/ordering-real-numbers",
    "AB6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-irrational-numbers/v/approximating-irrational-numbers",
    
    # Expressions and Equations - Additional Links
    "AC1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-exponents-properties/v/introduction-to-exponents",
    "AC2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-exponents-properties/v/negative-exponents",
    "AC3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-exponents-properties/v/multiplying-and-dividing-powers-with-integer-exponents",
    "AC4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-exponents-properties/v/quotient-of-powers",
    "AC5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-exponents-properties/v/powers-of-powers",
    "AC6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-exponents-properties/v/products-and-quotients-of-powers",
    "AC7": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-exponents-properties/v/simplifying-expressions-with-exponents",
    "AD1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-roots/v/introduction-to-square-roots",
    "AD2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-roots/v/understanding-square-roots",
    "AD3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-roots/v/square-roots-of-fractions",
    "AD4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-roots/v/introduction-to-cube-roots",
    "AD5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-roots/v/understanding-cube-roots",
    "AD6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-numbers-operations/cc-8th-roots/v/estimating-square-roots",
    "AD7": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-solving-equations-1/v/solving-quadratic-equations-by-taking-the-square-root",
    "AD8": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-solving-equations-1/v/solving-quadratic-equations-by-factoring",
    "AD9": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-solving-equations-1/v/solving-cubic-equations",
    
    # Linear Equations - Additional Links
    "AI1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-one-step-equations/v/solving-one-step-equations",
    "AI2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-two-step-equations/v/solving-two-step-equations",
    "AI3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-two-step-equations/v/solving-two-step-equations-2",
    "AI4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-equations-word-problems/v/solving-equations-word-problems",
    "AI5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-like-terms/v/combining-like-terms",
    "AI6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-variables-both-sides/v/solving-equations-with-variables-on-both-sides",
    "AI7": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-variables-both-sides/v/solving-equations-with-variables-on-both-sides-2",
    "AI8": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-variables-both-sides/v/solving-equations-with-decimals-and-fractions",
    "AI9": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/cc-8th-variables-both-sides/v/solving-equations-with-fractional-coefficients",
    
    # Functions - Additional Links
    "AQ1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-linear-equations-functions/cc-8th-function-intro/v/functions-part-1",
    "AQ2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-linear-equations-functions/cc-8th-function-intro/v/understanding-function-inputs-and-outputs-part-1",
    "AQ3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-linear-equations-functions/cc-8th-function-intro/v/evaluating-functions",
    "AQ4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-linear-equations-functions/cc-8th-function-intro/v/interpreting-function-graphs",
    "AQ5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-linear-equations-functions/cc-8th-function-intro/v/finding-inverse-functions",
    "AQ6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-linear-equations-functions/cc-8th-function-intro/v/completing-function-tables",
    "AQ7": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-linear-equations-functions/cc-8th-function-intro/v/domain-and-range-from-graphs",
    "AQ8": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-linear-equations-functions/cc-8th-function-intro/v/domain-of-a-function",
    "AQ9": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-linear-equations-functions/cc-8th-linear-functions-modeling/v/checking-if-a-point-is-a-solution-to-a-system-of-equations",
    
    # Systems of Equations - Additional Links
    "AM1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-solutions/v/verifying-solutions-to-systems",
    "AM2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-graphically/v/solving-systems-graphically",
    "AM3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-graphically/v/number-of-solutions-to-system-of-equations-graphically",
    "AM4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-graphically/v/interpreting-points-system-equations",
    "AM5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-graphically/v/understanding-solution-intersection",
    "AM6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-graphically/v/estimating-solutions-graphing",
    "AN1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-substitution/v/solving-systems-substitution",
    "AN2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-elimination/v/solving-systems-elimination",
    "AN3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-any-method/v/solving-systems-any-method",
    "AN4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-word-problems/v/solving-systems-by-inspection",
    "AN5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-solutions/v/number-of-solutions-algebraically",
    
    # Geometry - Additional Links
    "AZ1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-transformations-congruence/v/introduction-to-transformations",
    "AZ2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-transformations-congruence/v/describing-transformations",
    "AZ3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-transformations-congruence/v/performing-translations",
    "AZ4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-transformations-congruence/v/performing-rotations",
    "AZ5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-transformations-congruence/v/performing-reflections",
    "AZ6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-transformations-congruence/v/determining-translation-vector",
    "AZ7": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-transformations-congruence/v/determining-reflection-line",
    "AZ8": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-transformations-congruence/v/determining-center-angle-of-rotation",
    "AZ9": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-transformations-congruence/v/determining-transformation-rule",
    
    # Angle Relationships - Additional Links
    "BG1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-angles-parallel-lines/v/identifying-parallel-line-angles",
    "BG2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-angles-parallel-lines/v/finding-missing-angles-parallel-lines",
    "BG3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-angles-parallel-lines/v/solving-equations-parallel-lines",
    "BG4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-angles-parallel-lines/v/alternate-interior-angles",
    "BG5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-angles-parallel-lines/v/vertical-supplementary-angles",
    "BG6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-angles-parallel-lines/v/angle-relationships",
    "BG7": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-triangle-angles/v/triangle-angle-sum-proof",
    "BG8": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-triangle-angles/v/missing-angles-in-triangles",
    "BG9": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-triangle-angles/v/isosceles-triangle-angles",
    
    # More Geometry (Pythagorean Theorem and Volume)
    "BI1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/pythagorean-theorem-visual-proof",
    "BI2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/pythagorean-theorem-proof",
    "BI3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/pythagorean-theorem-1",
    "BI4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/pythagorean-theorem-2",
    "BI5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/pythagorean-theorem-3",
    "BI6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/converse-of-pythagorean-theorem",
    "BI7": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/pythagorean-theorem-word-problems",
    "BI8": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/perimeter-using-pythagorean-theorem",
    "BI9": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/area-using-pythagorean-theorem",
    "BJ1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/pythagorean-theorem-with-isosceles-triangles",
    "BJ2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/distance-formula-pythagorean-theorem",
    "BJ3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-pythagorean-theorem/v/distance-between-points",
    
    # Volume
    "BK1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/cylinder-volume-and-surface-area",
    "BK2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/cylinder-volume",
    "BK3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/solving-for-radius-given-cylinder-volume",
    "BK4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/cone-volume",
    "BK5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/volume-cone-example",
    "BK6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/solving-for-height-of-cone",
    "BK7": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/sphere-volume",
    "BK8": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/volume-of-a-sphere",
    "BK9": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/hemisphere-volume",
    "BL1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/comparing-cylinder-cone-sphere-volumes",
    "BL2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/volume-word-problems",
    "BL3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/cylinder-volume-surface-area-word-problem",
    "BL4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/volume-complex-shapes",
    "BL5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/interpreting-volume-functions",
    "BL6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-geometry/cc-8th-volume/v/scaling-volume",
    
    # Statistics
    "BM1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-scatter-plots/v/constructing-scatter-plot",
    "BM2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-scatter-plots/v/appropriate-axes-scale-scatter-plot",
    "BM3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-scatter-plots/v/interpreting-scatter-plots",
    "BM4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-scatter-plots/v/scatter-plot-trends",
    "BM5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-scatter-plots/v/positive-and-negative-correlations",
    "BM6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-scatter-plots/v/clustering-patterns-scatter-plots",
    "BM7": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-scatter-plots/v/outliers-scatter-plots",
    "BM8": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-scatter-plots/v/making-predictions-scatter-plots",
    
    # Lines of Best Fit
    "BN1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-line-of-best-fit/v/estimating-line-of-best-fit",
    "BN2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-line-of-best-fit/v/identifying-best-fit-lines",
    "BN3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-line-of-best-fit/v/judging-best-fit-lines",
    "BN4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-line-of-best-fit/v/estimating-equations-of-lines-of-best-fit",
    "BN5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-line-of-best-fit/v/making-predictions-with-linear-models",
    "BN6": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-line-of-best-fit/v/estimating-slope-of-line-of-best-fit",
    "BN7": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-line-of-best-fit/v/interpreting-slope-linear-models",
    "BN8": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-line-of-best-fit/v/interpreting-y-intercept-linear-models",
    "BN9": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-line-of-best-fit/v/writing-equations-for-lines-of-best-fit",
    "BO1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-line-of-best-fit/v/interpreting-linear-models-word-problems",
    
    # Two-Way Tables
    "BP1": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-two-way-tables/v/creating-two-way-tables",
    "BP2": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-two-way-tables/v/reading-two-way-tables",
    "BP3": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-two-way-tables/v/analyzing-two-way-tables",
    "BP4": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-two-way-tables/v/interpreting-two-way-tables",
    "BP5": "https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-data/cc-8th-two-way-tables/v/relative-frequency-two-way-tables"
}

# Common Core descriptions mapping
common_core_descriptions = {
    "8.NS.A.1": "Know that numbers that are not rational are called irrational. Understand informally that every number has a decimal expansion.",
    "8.NS.A.2": "Use rational approximations of irrational numbers to compare the size of irrational numbers.",
    "8.EE.A.1": "Know and apply the properties of integer exponents to generate equivalent numerical expressions.",
    "8.EE.A.2": "Use square root and cube root symbols to represent solutions to equations.",
    "8.EE.A.3": "Use numbers expressed in the form of a single digit times an integer power of 10.",
    "8.EE.A.4": "Perform operations with numbers expressed in scientific notation.",
    "8.EE.B.5": "Graph proportional relationships, interpreting the unit rate as the slope of the graph.",
    "8.EE.C.7": "Solve linear equations in one variable.",
    "8.EE.C.8": "Analyze and solve pairs of simultaneous linear equations.",
    "8.F.A.1": "Understand that a function is a rule that assigns to each input exactly one output.",
    "8.F.A.2": "Compare properties of two functions each represented in a different way.",
    "8.F.A.3": "Interpret the equation y = mx + b as defining a linear function.",
    "8.F.B.4": "Construct a function to model a linear relationship between two quantities.",
    "8.F.B.5": "Describe qualitatively the functional relationship between two quantities.",
    "8.G.A.1": "Verify experimentally the properties of rotations, reflections, and translations.",
    "8.G.A.2": "Understand that a two-dimensional figure is congruent to another if one can be obtained from the other by a sequence of rotations, reflections, and translations.",
    "8.G.A.3": "Describe the effect of dilations, translations, rotations, and reflections on two-dimensional figures using coordinates.",
    "8.G.A.4": "Understand that a two-dimensional figure is similar to another if one can be obtained from the other by a sequence of rotations, reflections, translations, and dilations.",
    "8.G.A.5": "Use informal arguments to establish facts about the angle sum and exterior angle of triangles.",
    "8.G.B.6": "Explain a proof of the Pythagorean Theorem and its converse.",
    "8.G.B.7": "Apply the Pythagorean Theorem to determine unknown side lengths in right triangles.",
    "8.G.B.8": "Apply the Pythagorean Theorem to find the distance between two points in a coordinate system.",
    "8.G.C.9": "Know the formulas for the volumes of cones, cylinders, and spheres and use them to solve real-world and mathematical problems.",
    "8.SP.A.1": "Construct and interpret scatter plots for bivariate measurement data.",
    "8.SP.A.2": "Know that straight lines are widely used to model relationships between two quantitative variables.",
    "8.SP.A.3": "Use the equation of a linear model to solve problems in the context of bivariate measurement data.",
    "8.SP.A.4": "Understand that patterns of association can also be seen in bivariate categorical data by displaying frequencies and relative frequencies in a two-way table."
}

# Difficulty ratings mapping (example)
difficulty_ratings = {
    "Introductory": 1,
    "Basic": 2,
    "Intermediate": 3,
    "Advanced": 4,
    "Challenging": 5
}

def generate_common_pitfalls(skill_description):
    """Generate common pitfalls for a skill."""
    return f"Students may have difficulty with {skill_description.lower()}, misunderstand key concepts, or make computational errors."

def generate_question_numbers():
    """Generate random but reasonable numbers of questions for each category."""
    return {
        "Concept / Introduction / Definition": random.randint(3, 7),
        "Practice": random.randint(9, 15),
        "Common Pitfall avoidance": random.randint(2, 5),
        "Application/word problem": random.randint(2, 6),
        "Challenging": random.randint(1, 3),
        "Total number of questions for each goal": 0  # Will be calculated later
    }

def process_skill(skill_id, skill_info):
    """Process a single skill and return its metadata."""
    # Get the Khan Academy URL if available
    khan_url = khan_academy_urls.get(skill_id, "")
    
    # Get example questions for this skill
    basic_questions = example_questions.get(skill_id, [])
    
    # Difficulty mapping (you can adjust these values)
    difficulty_mapping = {
        "AA": 3,  # Number System basics
        "AB": 4,  # Irrational numbers
        "AC": 4,  # Exponents
        "AD": 5,  # Square roots
        "AI": 4,  # Linear equations
        "AQ": 5,  # Functions
        "AZ": 5,  # Transformations
        "BI": 6,  # Pythagorean theorem
        "BK": 5,  # Volume
        "BM": 4,  # Statistics
    }
    
    # Get difficulty based on skill ID prefix (first two characters)
    difficulty = difficulty_mapping.get(skill_id[:2], 4)  # Default to 4 if not found
    
    # Map difficulty number to text
    difficulty_text_mapping = {
        1: "Introductory",
        2: "Basic",
        3: "Intermediate",
        4: "Advanced",
        5: "Challenging"
    }
    difficulty_text = difficulty_text_mapping.get(difficulty, "Intermediate")
    
    return {
        "id": f"{skill_info['standard_id']}.{skill_id}",
        "common_core_id": skill_info["standard_id"],
        "common_core_description": common_core_descriptions.get(skill_info["standard_id"], "Description not available"),
        "skill_name": skill_info["skill_description"],
        "skill_description": f"This skill requires students to {skill_info['skill_description'].lower()}",
        "khan_academy_topic": skill_info["skill_description"],
        "khan_academy_url": khan_url,
        "engage_ny_topic": f"Understanding and Applying {skill_info['skill_description']}",
        "ixl_topic": skill_info["skill_description"],
        "description": f"This skill focuses on helping students {skill_info['skill_description'].lower()}",
        "difficulty": difficulty_text,
        "difficulty_rating": difficulty,
        "basic_questions_example": basic_questions,
        "common_pitfalls": generate_common_pitfalls(skill_info["skill_description"]),
        "number_of_questions": generate_question_numbers()
    }

def process_json(input_file, output_file):
    """Process the input JSON file and create the unified format."""
    # Read the input JSON
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Process all skills
    unified_skills = []
    
    for unit in data:
        for cluster in unit["clusters"]:
            for sub_cluster in cluster["sub_clusters"]:
                for skill in sub_cluster["skills"]:
                    unified_skill = process_skill(skill["skill_id"], skill)
                    unified_skills.append(unified_skill)
    
    # Write the output JSON
    with open(output_file, 'w') as f:
        json.dump(unified_skills, f, indent=2)

def extract_questions_from_syllabus(syllabus_path):
    """Extract example questions from the syllabus markdown file."""
    with open(syllabus_path, 'r') as f:
        content = f.read()
    
    # Dictionary to store questions for each skill
    questions = {}
    
    # Find all sections with Core Example Questions
    sections = content.split('####')
    for section in sections[1:]:  # Skip first split which is before first ####
        # Get the skill name (first line)
        skill_name = section.strip().split('\n')[0].strip()
        
        # Find the Core Example Questions section
        if '* Core Example Questions:' in section:
            questions_part = section.split('* Core Example Questions:')[1].split('Difficulty:')[0]
            # Extract individual questions
            raw_questions = re.findall(r'\* (.*?)(?=\*|$)', questions_part, re.DOTALL)
            # Clean up the questions
            cleaned_questions = [q.strip().strip('*').strip() for q in raw_questions if q.strip()]
            
            # Map skill name to skill ID
            skill_id = skill_name_to_id.get(skill_name.lower())
            if skill_id:
                questions[skill_id] = cleaned_questions
    
    # For skills without questions in the syllabus, generate default questions
    for skill_id, skill_name in skill_id_to_name.items():
        if skill_id not in questions:
            questions[skill_id] = generate_default_questions(skill_id, skill_name)
    
    return questions

def generate_default_questions(skill_id, skill_name):
    """Generate default questions for skills that don't have questions in the syllabus."""
    # Default questions based on skill category (first two letters of skill_id)
    category = skill_id[:2]
    
    if category == "AC":  # Exponents
        return [
            f"Evaluate the expression using {skill_name.lower()}.",
            f"Apply {skill_name.lower()} to solve this problem.",
            f"Use {skill_name.lower()} to simplify the expression."
        ]
    elif category == "AD" or category == "AE":  # Square and Cube Roots
        return [
            f"Find the value using {skill_name.lower()}.",
            f"Solve the equation using {skill_name.lower()}.",
            f"Apply {skill_name.lower()} to solve this problem."
        ]
    elif category == "AF" or category == "AG":  # Scientific Notation
        return [
            f"Convert the number using {skill_name.lower()}.",
            f"Solve the problem using {skill_name.lower()}.",
            f"Apply {skill_name.lower()} to this situation."
        ]
    elif category == "AI":  # Linear Equations
        return [
            f"Solve the equation using {skill_name.lower()}.",
            f"Write and solve an equation for this word problem.",
            f"Apply {skill_name.lower()} to solve this problem."
        ]
    elif category == "AQ":  # Functions
        return [
            f"Given a function, {skill_name.lower()}.",
            f"Use {skill_name.lower()} to solve this problem.",
            f"Apply {skill_name.lower()} in this context."
        ]
    elif category == "AZ":  # Transformations
        return [
            f"Perform the transformation to {skill_name.lower()}.",
            f"Describe how to {skill_name.lower()}.",
            f"Apply {skill_name.lower()} to the given figure."
        ]
    elif category == "BI":  # Pythagorean Theorem
        return [
            f"Use the Pythagorean theorem to {skill_name.lower()}.",
            f"Solve this problem using {skill_name.lower()}.",
            f"Apply {skill_name.lower()} in this context."
        ]
    elif category == "BK":  # Volume
        return [
            f"Calculate the volume using {skill_name.lower()}.",
            f"Find the missing dimension using {skill_name.lower()}.",
            f"Apply {skill_name.lower()} to solve this problem."
        ]
    elif category == "BM":  # Statistics
        return [
            f"Create a scatter plot to {skill_name.lower()}.",
            f"Analyze the data to {skill_name.lower()}.",
            f"Use {skill_name.lower()} to interpret the data."
        ]
    else:
        return [
            f"Solve a problem involving {skill_name.lower()}.",
            f"Apply {skill_name.lower()} to this situation.",
            f"Use {skill_name.lower()} to solve this problem."
        ]

# Extract all skills from grade8topics.json
def extract_skills_from_topics(topics_json):
    """Extract all skills and their descriptions from the topics JSON."""
    skill_dict = {}
    
    def process_skills(skills):
        for skill in skills:
            skill_dict[skill["skill_description"].lower()] = skill["skill_id"]
    
    for unit in topics_json:
        for cluster in unit["clusters"]:
            for sub_cluster in cluster["sub_clusters"]:
                process_skills(sub_cluster["skills"])
    
    return skill_dict

# Load grade8topics.json
with open('/Users/binaydai/Downloads/grade8topics (1).json', 'r') as f:
    topics_json = json.load(f)

# Generate skill mappings
skill_name_to_id = extract_skills_from_topics(topics_json)
skill_id_to_name = {v: k for k, v in skill_name_to_id.items()}

# Extract questions from syllabus
example_questions = extract_questions_from_syllabus('/Users/binaydai/Downloads/Grade8Syllabus.md')

if __name__ == "__main__":
    # Use absolute path for input file
    input_file = "/Users/binaydai/Downloads/grade8topics (1).json"
    output_file = "unified_skills.json"
    process_json(input_file, output_file) 