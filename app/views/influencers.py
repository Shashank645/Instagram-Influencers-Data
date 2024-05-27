import pandas as pd
from fastapi import APIRouter
from starlette.responses import JSONResponse


class Influencer:
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
                if min_followers >= 1000000:
                    get_min_followers = "{:,.1f}m".format(min_followers / 1000000)
                    filtered_df = filtered_df[filtered_df['followers'] >= get_min_followers]
                else:
                    get_min_followers = "{:,.1f}m".format((min_followers / 1000000)*100)

                    filtered_df = filtered_df[filtered_df['followers'] >= get_min_followers]
            if min_avg_likes is not None:
                if min_avg_likes >= 1000000:
                    get_min_avg_likes = "{:,.1f}m".format(min_avg_likes / 1000000)
                else:
                    get_min_avg_likes = "{:,.0f}k".format(min_avg_likes / 1000)
                filtered_df = filtered_df[filtered_df['avg_likes'] >= get_min_avg_likes]
            if country is not None:
                filtered_df = filtered_df[filtered_df['country'] == country]
            filtered_df = filtered_df.map(
                lambda x: "" if isinstance(x, float) and (pd.isna(x) or not pd.isfinite(x)) else x)
            return JSONResponse(status_code=200, content=filtered_df.to_dict(orient='records'))

        return api_router
