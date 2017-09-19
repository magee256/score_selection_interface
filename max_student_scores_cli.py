import pandas as pd
import numpy as np
import argparse
import os.path


# Upload reference data
# Query with list of IDs
# Qualtrics master list

def CheckExt(ext_choices):
    """
    Checks if file exists and has an extension in ext_choices.

    Adapted from: https://stackoverflow.com/questions/15203829
    """
    class Act(argparse.Action):
        def __call__(self,parser,namespace,fname,option_string=None):
            if not os.path.exists(fname[0]):
                parser.error('file {} does not exist'
                        .format(fname[0]) )

            ext = os.path.splitext(fname[0])[1][1:].lower()
            if ext not in ext_choices:
                parser.error("file doesn't end with one of {}"
			.format(', '.join(ext_choices)) )
            else:
                setattr(namespace,self.dest,fname[0])

    return Act


def prep_input_args(args):
    """
    Process the user input arguments. Default parsing should be 
    handled here.
    """
    arg_dict = {
            'score_csv' : args.score_csv,
            'student_id_excel' : args.student_id_excel,
            }
    return arg_dict


def standardize_id_formats(x):
    """
    Convert IDs that are convertable to integer to integer. May add more
    advanced cleaning later
    """
    try:
        return int(x)
    except ValueError:
        return np.nan

def prepare_data(score_csv,student_id_excel):
    """
    Loading and cleaning up the data used for the analysis
    """
    score_df = pd.read_csv(score_csv,skiprows=1)
    score_df.rename(columns=lambda x: x.strip(),inplace=True)
    
    # Narrow to just data we're interested in
    score_df = score_df[['score','Enter your Student ID number:']]
    score_df.dropna(subset=['Enter your Student ID number:'],inplace=True)
    
    # Can coerce to standard form here, pick up badly formatted columns
    score_df['Enter your Student ID number:'] = \
            score_df['Enter your Student ID number:'].apply(standardize_id_formats)
    score_df.dropna(subset=['Enter your Student ID number:'],inplace=True)
    
    student_id_df = pd.read_excel(student_id_excel)
    return score_df, student_id_df

def write_max_scores(score_df,student_id_df):
    # Get just the Student IDs we're interested in
    sub_df = score_df[score_df['Enter your Student ID number:']
            .isin(student_id_df['Student ID'])]
    max_scores = sub_df.groupby('Enter your Student ID number:').max()
    max_scores.to_excel('max_scores.xlsx')

def max_student_scores(arg_dict):
    score_df, student_id_df = prepare_data(
            arg_dict['score_csv'],
            arg_dict['student_id_excel'],
            )
    write_max_scores(score_df,student_id_df)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=('Takes a file containing a'
            ' list of product ID\'s and the name of the website they were'
            ' taken from as argument. The program then scrapes all'
            ' product reviews and additional (site-dependent) information.'))
    
    parser.add_argument('score_csv', nargs=1, action=CheckExt(['csv']),
            help=('Path to CSV file containing scores'))
    parser.add_argument('student_id_excel', nargs=1, 
            action=CheckExt(['xlsx','xlsm']),
            help=('Path to Excel file containing the desired'
                ' student ID numbers.'))

    args = parser.parse_args()
    arg_dict = prep_input_args(args)
    max_student_scores(arg_dict)
