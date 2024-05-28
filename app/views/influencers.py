import pandas as pd
from fastapi import APIRouter
from starlette.responses import JSONResponse
from app.views.utils.influencers_utils import Influencer_details


class Influencer:
    influence_obj = Influencer_details()

    @property
    def router(self):
        api_router = APIRouter(prefix='/influencer')

        @api_router.get('/filter')
        def get_influencer_data(min_influence_score: int = None, min_followers: int = None, min_avg_likes: float = None,
                                country: str = None):
            df = pd.read_csv('top_insta_influencers_data.csv')
            filtered_df = df.copy()

            if min_influence_score is not None:
                filtered_df = filtered_df[filtered_df['influence_score'] >= min_influence_score]
            if min_followers is not None:
                filtered_df["followers_numeric"] = filtered_df["followers"]
                for index, follow_str in enumerate(filtered_df['followers_numeric']):
                    followers_numeric = self.influence_obj.to_numeric(follow_str)
                    filtered_df["followers_numeric"][index] = followers_numeric
                filtered_df = filtered_df[filtered_df['followers_numeric'] >= min_followers]

            if min_avg_likes is not None:
                filtered_df["average_numeric"] = filtered_df["avg_likes"]
                for index, avg_str in enumerate(filtered_df['average_numeric']):
                    avg_numeric = self.influence_obj.to_numeric(avg_str)
                    filtered_df["average_numeric"][index] = avg_numeric
                filtered_df = filtered_df[filtered_df['average_numeric'] >= min_avg_likes]
            if country is not None:
                filtered_df = filtered_df[filtered_df['country'] == country]
            filtered_df = filtered_df.map(
                lambda x: "" if isinstance(x, float) and (pd.isna(x) or not pd.isfinite(x)) else x)
            return JSONResponse(status_code=200, content=filtered_df.to_dict(orient='records'))

        return api_router
