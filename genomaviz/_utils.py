def _binarize_col(row, median):
    if row <= median:
        return 0
    elif row > median:
        return 1
    return ""


def _quartilize_col(row, q1, q2, q3):
    if row <= q1:
        return 1
    elif row <= q2:
        return 2
    elif row <= q3:
        return 3
    elif row > q3:
        return 4
    else:
        return ""


def _recommendation_col(row, fit):
    if row[fit]>=85:
        return "Recomendado"
    elif row[fit]>=60:
        return "Quizás"
    elif row[fit]<60:
        return "No recomendado"


def _get_date_dif(row, col1, col2):
  if row["date_added"]:
    if "time"=="day":
        return (pd.to_datetime(row[col1]) - pd.to_datetime(row[col2])).days
    elif "time"=="months":
        return (pd.to_datetime(row[col1]) - pd.to_datetime(row[col2])).month
    elif "time"=="years":
        return (pd.to_datetime(row[col1]) - pd.to_datetime(row[col2])).months/12
  else:
    return ""