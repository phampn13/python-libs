import pandas as pd

def lp_df_sum(df, type='spec', line_width=100, columns=None):
    """
    This function discovers information about the given Pandas DataFrame.

    Parameters:
    - df: Pandas DataFrame
    - type: str, optional ('spec' or 'data')
      - 'spec': Display general information about the DataFrame.
      - 'data': Display distinct values for specified columns.
    - line_width: int, optional
      - Maximum width of lines in the output.
    - columns: list, optional
      - List of column names to show distinct values for (only for type='data').

    Returns:
    - None: Prints the summary information.

    Raises:
    - ValueError: If type or line_width has an invalid value.
    - KeyError: If a specified column does not exist in the DataFrame.
    """

    # Validation
    if type not in ['spec', 'data']:
        raise ValueError("Error: type is invalid. It must be 'spec' or 'data'.")

    if not isinstance(line_width, int):
        raise ValueError("Error: line_width must be an integer.")

    if line_width < 80:
        line_width = 80

    if not isinstance(columns, list) and columns is not None:
        raise ValueError("Error: columns must be a list of column names.")

    # Check for duplicated rows in a DataFrame
    def has_duplicates(df):
        return any(df.duplicated() | df.duplicated(keep='last'))

    # Convert the list of values to a string
    def get_distinct_values(column_values):
        unique_values = sorted(column_values.unique(), key=lambda x: (0, '') if pd.isna(x) else (1, x))

        output = []
        
        total_values = len(unique_values)
        
        for i, current_value in enumerate(unique_values):
            current_value_str = str(current_value)
            
            if not output:
                output.append(current_value_str)
            else:
                current_output = ', '.join(output + [current_value_str])
                if len(current_output) <= line_width:
                    output.append(current_value_str)
                else:
                    output.append('...')
                    break
        
        return f"({', '.join(output)}) ({total_values} values)"

    # Build the result string
    result = ""

    # Spec
    if type == 'spec':
        duplicates = has_duplicates(df)

        result += f"***** Data Frame: {df.shape[1]} columns x {df.shape[0]} rows"
        result += ", duplicates: yes" if duplicates else ", duplicates: no"

        for i, col_name in enumerate(df.columns, start=1):
            col_type = df[col_name].dtype
            has_na = df[col_name].isna().any()
            is_unique = len(df[col_name].unique()) == df.shape[0]

            result += f"\n{i}. {col_name}: {col_type}"
            result += ", NA: yes" if has_na else ", NA: no"
            result += ", Unique: yes" if is_unique else ", Unique: no"

    # Distinct Values
    elif type == 'data':
        duplicates = has_duplicates(df)

        result += f"***** Sorted Distinct Values: {df.shape[1]} columns x {df.shape[0]} rows"
        result += ", duplicates: yes" if duplicates else ", duplicates: no"

        if columns is None:
            columns = df.columns

        for i, col_name in enumerate(columns, start=1):
            if col_name in df.columns:
                col_index = df.columns.get_loc(col_name) + 1  # Find the index of the column
                distinct_values = get_distinct_values(df[col_name])
                result += f"\n{col_index}. {col_name}\n{distinct_values}"
            else:
                result += f"\nWarning: Column '{col_name}' not found in the data frame."

    # Print the result string
    print(result)
