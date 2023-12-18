# Arciaga - PyCity Schools Analysis

# Import Dependencies and Setup
import pandas as pd
from pathlib import Path

# Store filepaths into variables 
school_data_to_load = Path("schools_complete.csv")
student_data_to_load = Path("students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()

# Calculate the total number of unique schools
school_count = school_data["school_name"].nunique()
school_count

# Calculate the total number of students
student_count = student_data["student_name"].count()
student_count

# Calculate the total budget
total_budget = school_data["budget"].sum()
total_budget

# Calculate the average (mean) math score
average_math_score = student_data["math_score"].mean()
average_math_score

# Calculate the average (mean) reading score
average_reading_score = student_data["reading_score"].mean()
average_reading_score

# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage

# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)  
passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage

# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate

# Create a high-level snapshot of the district's key metrics in a DataFrame
district_summary = pd.DataFrame({
    "Total Schools": [school_count],
    "Total Students": [student_count],
    "Total Budget": [total_budget],
    "Average Math Score": [average_math_score],
    "Average Reading Score": [average_reading_score],
    "Passing Math %": [passing_math_percentage],  
    "Passing Reading %": [passing_reading_percentage],
    "Overall Passing Rate": [overall_passing_rate]
})

# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)

# Display the DataFrame
(district_summary)

# Arciaga - School Summary

# Use the code provided to select all of the school types
school_types = school_data["type"].unique()
print (school_types)

# Calculate the total student count per school
per_school_counts = student_data["school_name"].value_counts()
print (per_school_counts)

# Calculate the total student count per school
per_school_counts = student_data["school_name"].value_counts()
per_school_counts

# Calculate the total school budget and per capita spending per school
per_school_budget = school_data.groupby("school_name")["budget"].first()
per_school_capita = per_school_budget / per_school_counts
print (per_school_budget)
print (per_school_capita)

# Calculate the average test scores per school
per_school_math = student_data.groupby("school_name")["math_score"].mean()
per_school_reading = student_data.groupby("school_name")["reading_score"].mean()
print (per_school_math)
print (per_school_reading)

# Calculate the number of students per school with math scores of 70 or higher
students_passing_math = student_data[student_data["math_score"] >= 70]
school_students_passing_math = students_passing_math.groupby("school_name")["Student ID"].count()
school_students_passing_math

# Calculate the number of students per school with reading scores of 70 or higher
students_passing_reading = student_data[student_data["reading_score"] >= 70]
school_students_passing_reading = students_passing_reading.groupby("school_name")["Student ID"].count()
school_students_passing_reading

# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher
students_passing_math_and_reading = school_data_complete[
    (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)
]
school_students_passing_math_and_reading = students_passing_math_and_reading.groupby(["school_name"]).size()
school_students_passing_math_and_reading

# Use the provided code to calculate the passing rates
per_school_passing_math = school_students_passing_math / per_school_counts * 100
per_school_passing_reading = school_students_passing_reading / per_school_counts * 100
overall_passing_rates = school_students_passing_math_and_reading / per_school_counts * 100
print (per_school_passing_math)
print (per_school_passing_reading)
print (overall_passing_rates)

# Set school types index for upcoming dataframe 
schooltypes= school_data[["type","school_name"]].set_index("school_name")["type"]
schooltypes

# Create a DataFrame called `per_school_summary` with columns for the calculations above.
per_school_summary = pd.DataFrame({
    "School Types": schooltypes,
    "Total Students": per_school_counts,
    "Total School Budget": per_school_budget,
    "Per Student Budget": per_school_capita,
    "Average Math Score": per_school_math,
    "Average Reading Score": per_school_reading,  
    "% Passing Math": per_school_passing_math,
    "% Passing Reading": per_school_passing_reading,
    "% Overall Passing": overall_passing_rates
})

# Formatting
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the DataFrame
per_school_summary

# Arciaga - Highest-Performing Schools (by % Overall Passing)

# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values("% Overall Passing", ascending=False)
top_schools.head(5)

# Arciaga - Bottom Performing Schools (By % Overall Passing)

# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values("% Overall Passing", ascending=True)
bottom_schools.head(5)

# Arciaga - Math Scores by Grade

# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by `school_name` and take the mean of the `math_score` column for each.
ninth_grade_math_scores = ninth_graders.groupby("school_name")["math_score"].mean()
tenth_grade_math_scores = tenth_graders.groupby("school_name")["math_score"].mean()
eleventh_grade_math_scores = eleventh_graders.groupby("school_name")["math_score"].mean()
twelfth_grade_math_scores = twelfth_graders.groupby("school_name")["math_score"].mean()

# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade = pd.DataFrame({
    "9th Grade": ninth_grade_math_scores, 
    "10th Grade": tenth_grade_math_scores,
    "11th Grade": eleventh_grade_math_scores,
    "12th Grade": twelfth_grade_math_scores
})

# Minor data wrangling
math_scores_by_grade.index.name = None

# Display the DataFrame
math_scores_by_grade

# Arciaga - Reading Score by Grade

# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by `school_name` and take the mean of the the `reading_score` column for each.
ninth_grade_reading_scores = ninth_graders.groupby("school_name")["reading_score"].mean()
tenth_grade_reading_scores = tenth_graders.groupby("school_name")["reading_score"].mean()
eleventh_grade_reading_scores = eleventh_graders.groupby("school_name")["reading_score"].mean()
twelfth_grade_reading_scores = twelfth_graders.groupby("school_name")["reading_score"].mean()

# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.DataFrame({
    "9th Grade": ninth_grade_reading_scores, 
    "10th Grade": tenth_grade_reading_scores,
    "11th Grade": eleventh_grade_reading_scores,
    "12th Grade": twelfth_grade_reading_scores
})

# Minor data wrangling
reading_scores_by_grade = reading_scores_by_grade[["9th Grade", "10th Grade", "11th Grade", "12th Grade"]]
reading_scores_by_grade.index.name = None

# Display the DataFrame
reading_scores_by_grade

# Arciaga - Scores by School Spending

# Establish the bins 
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]

# Create a copy of the school summary since it has the "Per Student Budget" 
school_spending_df = per_school_summary.copy()

# Use `pd.cut` to categorize spending based on the bins.
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(
    per_school_capita,
    bins=spending_bins,
    labels=labels,
    include_lowest=True
)
school_spending_df

#  Calculate averages for the desired columns. 
spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Math Score"].mean()
spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Reading Score"].mean()
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Math"].mean()
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Reading"].mean()
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Overall Passing"].mean()
print (spending_math_scores)
print (spending_reading_scores)
print (spending_passing_math)
print (spending_passing_reading)
print (overall_passing_spending)

# Assemble into DataFrame
spending_summary = pd.DataFrame({
    "Average Math Score": spending_math_scores,
    "Average Reading Score": spending_reading_scores,
    "% Passing Math": spending_passing_math,
    "% Passing Reading": spending_passing_reading,
    "% Overall Passing": overall_passing_spending
})

# Display results
spending_summary

# Arciaga - Scores by School Size

# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

per_school_summary["School Size"] = pd.cut(
    per_school_summary["Total Students"],
    bins=size_bins,
    labels=labels,
    right=False
)
per_school_summary

# Calculate averages for the desired columns. 
size_math_scores = per_school_summary.groupby(["School Size"])["Average Math Score"].mean()
size_reading_scores = per_school_summary.groupby(["School Size"])["Average Reading Score"].mean()
size_passing_math = per_school_summary.groupby(["School Size"])["% Passing Math"].mean()
size_passing_reading = per_school_summary.groupby(["School Size"])["% Passing Reading"].mean()
size_overall_passing = per_school_summary.groupby(["School Size"])["% Overall Passing"].mean()
print (size_math_scores)
print (size_reading_scores)
print (size_passing_math)
print (size_passing_reading)
print (size_overall_passing)

# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = pd.DataFrame({
    "Average Math Score": size_math_scores,
    "Average Reading Score": size_reading_scores,
    "% Passing Math": size_passing_math,
    "% Passing Reading": size_passing_reading,
    "% Overall Passing": size_overall_passing
})

# Display results
size_summary

# Arciaga - Scores by School Type

# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = per_school_summary.groupby(["School Types"])["Average Math Score"].mean()
average_reading_score_by_type = per_school_summary.groupby(["School Types"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(["School Types"])["% Passing Math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(["School Types"])["% Passing Reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(["School Types"])["% Overall Passing"].mean()

# Assemble the new data by type into a DataFrame called `type_summary`
type_summary = pd.DataFrame({
    "Average Math Score": average_math_score_by_type,
    "Average Reading Score": average_reading_score_by_type,
    "% Passing Math": average_percent_passing_math_by_type,
    "% Passing Reading": average_percent_passing_reading_by_type,
    "% Overall Passing": average_percent_overall_passing_by_type
})

# Display results
type_summary