import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import scale, normalize

class SimilarityCalculator(object):
    def __init__(self, data_dir, weights={'interests': 1, 'assessment_scores': 1, 'tag_view_time': 1}):
        self.data_dir = data_dir
        self.weights = weights
    
    def data_file_path(self, filename):
        return os.path.join(self.data_dir, filename)
        
    @property
    def user_interests_file(self):
        return self.data_file_path('user_interests.csv')
    
    @property
    def user_assessment_scores_file(self):
        return self.data_file_path('user_assessment_scores.csv')
        
    @property
    def user_course_views_file(self):
        return self.data_file_path('user_course_views.csv')
        
    @property
    def course_tags_file(self):
        return self.data_file_path('course_tags.csv')
        
    @property
    def user_interests_data(self):
        """Construct a dataframe indicating which users have which interest."""
        interests = pd.read_csv(self.user_interests_file, usecols=['user_handle', 'interest_tag'])\
            .drop_duplicates()\
            .assign(value=1)\
            .pivot(index='user_handle', columns='interest_tag', values='value').fillna(0)
        return interests
        
    @property
    def user_assessment_scores_data(self):
        """Take the most recent score for each assessment and standardize."""
        scores = pd.read_csv(self.user_assessment_scores_file, parse_dates=['user_assessment_date'])\
            .sort_values(by=['user_handle', 'assessment_tag', 'user_assessment_date'])\
            .drop_duplicates(subset=['user_handle', 'assessment_tag'], keep='last')\
            .pivot(index='user_handle', columns='assessment_tag', values='user_assessment_score')
        return ((scores - 140) / 60).fillna(0)
    
    @property 
    def user_tag_view_time_data(self):
        """Compute and scale the amount of time that each user spent watching videos with each tag"""
        user_course_views = pd.read_csv(self.user_course_views_file)
        course_tags = pd.read_csv(self.course_tags_file)
        tag_times = user_course_views.merge(course_tags, on='course_id', how='inner')\
            .groupby(['user_handle', 'course_tags'], as_index=False).view_time_seconds.sum()
        pivoted = tag_times.pivot(index='user_handle', columns='course_tags', values='view_time_seconds').fillna(0)
        return pd.DataFrame(data=scale(pivoted), index=pivoted.index, columns=pivoted.columns)
        
    @property
    def all_features(self):
        """Put together the 3 types of features. """
        weights = self.weights
        interests = weights['interests'] * self.user_interests_data.rename(columns=lambda x: "int_{}".format(x))
        assessments = weights['assessment_scores'] * self.user_assessment_scores_data.rename(columns=lambda x: "assess_{}".format(x))
        tag_view_time = weights['tag_view_time'] * self.user_tag_view_time_data.rename(columns=lambda x: "view_{}".format(x))
        return pd.concat([interests, assessments, tag_view_time], axis=1).fillna(0)
        
    @property
    def scores(self):
        """Compute the similarity matrix by normalizing the rows and taking the data covariance."""
        features = self.all_features
        handles = features.index
        normalized = normalize(features.values)
        return pd.DataFrame(data=np.dot(normalized, normalized.T), index=handles, columns=handles)
    
    def most_similar(self, scores, user_handle, n=10):
        """Identify the highest similarity scores for a given user."""
        summary = scores.loc[:,[user_handle]]\
            .nlargest(n + 1, columns=user_handle)\
            .drop(labels=user_handle, axis=0)\
            .head(n=n)\
            .reset_index()\
            .rename(columns={user_handle: 'score'})
        return summary
    
    @property
    def all_summaries(self, n=10):
        scores = self.scores
        records = [(user, self.most_similar(scores, user, n).to_json(orient='index')) for user in scores.index]
        return pd.DataFrame.from_records(records, columns=['user_handle', 'most_similar'])
    
    
    