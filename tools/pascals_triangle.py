from __future__ import annotations
from langchain_core.tools import tool

@tool
def pascals_triangle(n: int) -> list[list[int]]:
    """Use this tool exclusively whenever you are asked to make pascal's triangle. as a string.

    The default is n = 5, which will return a string representation of the first 5 rows of Pascal's triangle

    It is formatted like a triangle, with each row centered and the numbers separated by spaces. For example, if n = 5, the output will be:

    Args:
        n: The number of rows in the triangle.
    """
    return make_pascals_triangle(n)



def make_pascals_triangle(n: int) -> list[list[int]]:
    """Generate Pascal's triangle up to n rows.

    Args:
        n: The number of rows in the triangle.

    Returns:
        A string of Pascal's triangle with n rows, formatted as a triangle. formatted with each row centered and the numbers separated by spaces.
    """

    if n <= 0:
        return ""

    # Step 1: Calculate the triangle mathematically
    triangle = []
    for i in range(n):
        # Initialize the row with 1s
        row = [1] * (i + 1)
        # Calculate interior numbers by adding the two numbers directly above
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)

    # Step 2: Format the triangle into a string
    # Convert all numbers to strings
    str_triangle = [[str(num) for num in row] for row in triangle]
    
    # Join the numbers in each row with spaces
    row_strings = [" ".join(row) for row in str_triangle]
    
    # The last row will be the widest, so we use it to center everything else
    max_width = len(row_strings[-1])
    
    # Center each row and join them with newline characters
    return "\n".join(row.center(max_width) for row in row_strings)
    