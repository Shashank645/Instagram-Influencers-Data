import pandas as pd
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.views.utils.influencers_utils import InfluencerDetails


class Influencer:
    influence_obj = InfluencerDetails()

    @property
    def router(self):
        """
               Property to create and return an API router for the Influencer class.
               """
        api_router = APIRouter()

        @api_router.get('/filter')
        def get_filter_influencer_data(min_influence_score: int = None, min_followers: int = None,
                                       min_avg_likes: float = None,
                                       country: str = None):
            """
                     Endpoint to filter influencer data based on provided query parameters.\n
                     :param min_influence_score: Minimum influence score for filtering influencers.\n
                     :param min_followers: Minimum number of followers for filtering influencers.\n
                     :param min_avg_likes: Minimum average likes for filtering influencers.\n
                     :param country: Country for filtering influencers.\n
                     :return: Filtered influencer data in JSON format.
                     """
            try:
                df = pd.read_csv('top_insta_influencers_data.csv')
                filtered_df = df.copy()
            except Exception as err:
                raise HTTPException(status_code=404, detail="File not found " + str(err))

            if min_influence_score is not None:
                # Filter by minimum influence score
                filtered_df = filtered_df[filtered_df['influence_score'] >= min_influence_score]

            if min_followers is not None:
                try:
                    # Convert followers to numeric values
                    filtered_df['followers_numeric'] = filtered_df['followers'].apply(self.influence_obj.to_numeric)
                    # Filter by minimum number of followers
                    filtered_df = filtered_df[filtered_df['followers_numeric'] >= min_followers]
                except Exception as err:
                    raise HTTPException(status_code=400, detail="Error processing followers data: " + str(err))

            if min_avg_likes is not None:
                try:
                    # Convert average likes to numeric values
                    filtered_df['average_numeric'] = filtered_df['avg_likes'].apply(self.influence_obj.to_numeric)
                    # Filter by minimum average likes
                    filtered_df = filtered_df[filtered_df['average_numeric'] >= min_avg_likes]
                except Exception as err:
                    raise HTTPException(status_code=400, detail="Error processing average likes data: "+str(err))

            if country is not None:
                # Filter by country
                filtered_df = filtered_df[filtered_df['country'] == country]
            # Handle missing or non-finite values
            filtered_df = filtered_df.map(
                lambda x: "" if isinstance(x, float) and (pd.isna(x) or not pd.isfinite(x)) else x)
            # Convert filtered DataFrame to JSON response
            return JSONResponse(status_code=200, content=filtered_df.to_dict(orient='records'))

        return api_router
