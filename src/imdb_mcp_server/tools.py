import json
from typing import Any, Dict, List, Literal, Optional
from mcp.server.fastmcp import Context

from .api import make_imdb_request, paginated_response, BASE_URL


def register_tools(mcp):
    """Register all MCP tools with the server."""
    
    # -----------------------------SEARCH TOOLS-----------------------------------
    
    @mcp.tool()     
    async def search_imdb(
        ctx: Context,
        original_title: Optional[str] = None,
        original_title_autocomplete: Optional[str] = None,
        primary_title: Optional[str] = None,
        primary_title_autocomplete: Optional[str] = None,
        type: Optional[str] = None,
        genre: Optional[str] = None,
        genres: Optional[List[str]] = None,
        is_adult: Optional[bool] = None,
        average_rating_from: Optional[float] = None,
        average_rating_to: Optional[float] = None,
        num_votes_from: Optional[int] = None,
        num_votes_to: Optional[int] = None,
        start_year_from: Optional[int] = None,
        start_year_to: Optional[int] = None,
        countries_of_origin: Optional[List[str]] = None,
        spoken_languages: Optional[List[str]] = None,
        sort_order: Optional[Literal["ASC", "DESC"]] = None,
        sort_field: Optional[Literal["id", "averageRating", "numVotes", "startYear"]] = None,
        ) -> str:
        """Search for movies on IMDb. First 5 results are returned.
        Args:
            original_title: The original title of the movie to search for. Searches the whole word.
            original_title_autocomplete: The autocomplete title of the movie to search for. Searches the partial word.
            primary_title: The primary title of the movie to search for. Searches the whole word.
            primary_title_autocomplete: The autocomplete primary title of the movie to search for. Searches the partial word.
            type: The type of the movie to search for. Get all possible types with get_types().
            genre: The genre of the movie to search for. Get all possible genres with get_genres().
            genres: The genres of the movie to search for. List of Genres. Get all possible genres with get_genres().
            is_adult: Whether to include adult movies in the search results.
            average_rating_from: The minimum average rating of the movie to search for.
            average_rating_to: The maximum average rating of the movie to search for.
            num_votes_from: The minimum number of votes of the movie to search for.
            num_votes_to: The maximum number of votes of the movie to search for.
            start_year_from: The minimum start year of the movie to search for.
            start_year_to: The maximum start year of the movie to search for.
            countries_of_origin: The countries of origin of the movie to search for. In ISO 3166-1 alpha-2 format list of strings. Get all possible countries with get_countries().
            spoken_languages: The spoken languages of the movie to search for. In ISO 639-1 format list of strings. Get all possible languages with get_languages().
            sort_order: The order of the search results. Possible values: "ASC", "DESC".
            sort_field: The field to sort the search results by. Possible values: "id", "averageRating", "numVotes", "startYear".
        Returns:
            JSON object containing the first 5 search results.
        """
        search_url = f"{BASE_URL}/search"
        search_data = await make_imdb_request(search_url, {"originalTitle": original_title,
                                                           "originalTitleAutocomplete": original_title_autocomplete,
                                                           "primaryTitle": primary_title,
                                                           "primaryTitleAutocomplete": primary_title_autocomplete,
                                                           "type": type,
                                                           "genre": genre,
                                                           "genres": genres,
                                                           "isAdult": is_adult,
                                                           "averageRatingFrom": average_rating_from, 
                                                           "averageRatingTo": average_rating_to,
                                                           "numVotesFrom": num_votes_from,
                                                           "numVotesTo": num_votes_to,
                                                           "startYearFrom": start_year_from,
                                                           "startYearTo": start_year_to,
                                                           "countriesOfOrigin": countries_of_origin,
                                                           "spokenLanguages": spoken_languages,
                                                           "sortOrder": sort_order,
                                                           "sortField": sort_field}, ctx)
        if not search_data or not search_data.get("results", []):
            return "Unable to fetch search data for this movie or movie not found."
        
        search_results = search_data.get("results", [])[:5]
        return json.dumps(search_results, indent=4)


    # -----------------------------IMDB ID TOOLS-----------------------------------

    @mcp.tool()
    async def get_imdb_details(imdb_id: str, ctx: Context) -> str:
        """Get more in depth details about a movie/series from IMDb.
        Args:
            imdbId: The IMDb ID of the movie/series to get details for.
        Returns:
            JSON object containing the movie/series details.
        """
        imdb_details_url = f"{BASE_URL}/{imdb_id}"
        imdb_details_data = await make_imdb_request(imdb_details_url, {}, ctx)
        if not imdb_details_data:
            return "Unable to fetch imdb details data for this movie or movie not found."
        return json.dumps(imdb_details_data, indent=4)


    @mcp.tool()
    async def get_directors(imdb_id: str, ctx: Context) -> str:
        """Get the directors of a movie from IMDb.
        Args:
            imdbId: The IMDb ID of the movie to get directors for.
        Returns:
            JSON object containing the directors of the movie.
        """
        directors_url = f"{BASE_URL}/{imdb_id}/directors"
        directors_data = await make_imdb_request(directors_url, {}, ctx)
        if not directors_data:
            return "Unable to fetch directors data for this movie or movie not found."
        return json.dumps(directors_data, indent=4)

        
    @mcp.tool()
    async def get_cast(imdb_id: str, ctx: Context) -> str:
        """Get the cast of a movie from IMDb.
        Args:
            imdbId: The IMDb ID of the movie to get cast for.
        Returns:
            JSON object containing the cast of the movie.
        """
        cast_url = f"{BASE_URL}/{imdb_id}/cast"
        cast_data = await make_imdb_request(cast_url, {}, ctx)
        if not cast_data:
            return "Unable to fetch cast data for this movie or movie not found."
        return json.dumps(cast_data, indent=4)


    @mcp.tool()
    async def get_writers(imdb_id: str, ctx: Context) -> str:
        """Get the writers of a movie from IMDb.
        Args:
            imdbId: The IMDb ID of the movie to get writers for.
        Returns:
            JSON object containing the writers of the movie.
        """
        writers_url = f"{BASE_URL}/{imdb_id}/writers"
        writers_data = await make_imdb_request(writers_url, {}, ctx)
        if not writers_data:
            return "Unable to fetch writers data for this movie or movie not found."
        return json.dumps(writers_data, indent=4)


    # -----------------------------CONFIGURATION TOOLS-----------------------------------

    @mcp.tool()
    async def get_types(ctx: Context) -> str:
        """Get all types.
        Returns:
            JSON object containing all types.
        """
        types_url = f"{BASE_URL}/types"
        types_data = await make_imdb_request(types_url, {}, ctx)
        if not types_data:
            return "Unable to fetch types data."
        return json.dumps(types_data, indent=4)

    @mcp.tool()
    async def get_genres(ctx: Context) -> str:
        """Get all genres.
        Returns:
            JSON object containing all genres.
        """
        genres_url = f"{BASE_URL}/genres"
        genres_data = await make_imdb_request(genres_url, {}, ctx)
        if not genres_data:
            return "Unable to fetch genres data."
        return json.dumps(genres_data, indent=4)


    @mcp.tool()
    async def get_countries(ctx: Context) -> str:
        """Get all countries.
        Returns:
            JSON object containing all countries.
        """
        countries_url = f"{BASE_URL}/countries"
        countries_data = await make_imdb_request(countries_url, {}, ctx)
        if not countries_data:
            return "Unable to fetch countries data."
        return json.dumps(countries_data, indent=4)


    @mcp.tool()
    async def get_languages(ctx: Context) -> str:
        """Get all languages.
        Returns:
            JSON object containing all languages.
        """
        languages_url = f"{BASE_URL}/languages"
        languages_data = await make_imdb_request(languages_url, {}, ctx)
        if not languages_data:
            return "Unable to fetch languages data."
        return json.dumps(languages_data, indent=4)


    # -----------------------------MOVIES TOOLS-----------------------------------

    @mcp.tool()
    async def get_top_250_movies(start: int, ctx: Context) -> str:
        """Get the top 250 movies from IMDb with pagination.
        Args:
            start: The starting index (0-based) to retrieve movies from.
        Returns:
            JSON object containing 5 top movies starting from the specified index.
        """
        top_250_url = f"{BASE_URL}/top250-movies"
        top_250_data = await make_imdb_request(top_250_url, {}, ctx)
        if not top_250_data:
            return "Unable to fetch top 250 movies data."
        return json.dumps(paginated_response(top_250_data, start, len(top_250_data)), indent=4)


    @mcp.tool()
    async def get_top_box_office_us(start: int, ctx: Context) -> str:
        """Get the top box office data for the US from IMDb with pagination.
        Args:
            start: The starting index (0-based) to retrieve movies from.
        Returns:
            JSON object containing 5 top box office movies starting from the specified index.
        """
        box_office_us_url = f"{BASE_URL}/top-box-office"
        box_office_us_data = await make_imdb_request(box_office_us_url, {}, ctx)
        if not box_office_us_data:
            return "Unable to fetch box office data for the US."
        return json.dumps(paginated_response(box_office_us_data, start, len(box_office_us_data)), indent=4)


    @mcp.tool()
    async def get_most_popular_movies(start: int, ctx: Context) -> str:
        """Get the most popular movies from IMDb with pagination.
        Args:
            start: The starting index (0-based) to retrieve movies from.
        Returns:
            JSON object containing 5 most popular movies starting from the specified index.
        """
        most_popular_movies_url = f"{BASE_URL}/most-popular-movies"
        most_popular_movies_data = await make_imdb_request(most_popular_movies_url, {}, ctx) 
        if not most_popular_movies_data:
            return "Unable to fetch most popular movies data."
        return json.dumps(paginated_response(most_popular_movies_data, start, len(most_popular_movies_data)), indent=4)


    # -----------------------------TV SHOWS TOOLS-----------------------------------

    @mcp.tool()
    async def get_top_250_tv_shows(start: int, ctx: Context) -> str:
        """Get the top 250 TV shows from IMDb with pagination.
        Args:
            start: The starting index (0-based) to retrieve TV shows from.
        Returns:
            JSON object containing 5 top TV shows starting from the specified index.
        """
        top_250_tv_shows_url = f"{BASE_URL}/top250-tv"
        top_250_tv_shows_data = await make_imdb_request(top_250_tv_shows_url, {}, ctx)
        if not top_250_tv_shows_data:
            return "Unable to fetch top 250 TV shows data."
        return json.dumps(paginated_response(top_250_tv_shows_data, start, len(top_250_tv_shows_data)), indent=4)


    @mcp.tool()
    async def get_most_popular_tv_shows(start: int, ctx: Context) -> str:
        """Get the most popular TV shows from IMDb with pagination.
        Args:
            start: The starting index (0-based) to retrieve TV shows from.
        Returns:
            JSON object containing 5 most popular TV shows starting from the specified index.
        """
        most_popular_tv_shows_url = f"{BASE_URL}/most-popular-tv"
        most_popular_tv_shows_data = await make_imdb_request(most_popular_tv_shows_url, {}, ctx)
        if not most_popular_tv_shows_data:
            return "Unable to fetch most popular TV shows data."
        return json.dumps(paginated_response(most_popular_tv_shows_data, start, len(most_popular_tv_shows_data)), indent=4)


    # -----------------------------UPCOMING RELEASES TOOLS-----------------------------------

    @mcp.tool()
    async def get_upcoming_releases(country_code: str, type: str, start: int, ctx: Context) -> str:
        """Get the upcoming releases from IMDb with pagination.
        Args:
            country_code: The country code to get the upcoming releases for.
            type: The type of the upcoming releases to get. Possible values: "TV", "MOVIE".
            start: The starting index (0-based) to retrieve releases from.
        Returns:
            JSON object containing 5 upcoming releases starting from the specified index.
        """
        upcoming_releases_url = f"{BASE_URL}/upcoming-releases"
        upcoming_releases_data = await make_imdb_request(upcoming_releases_url, {"countryCode": country_code, "type": type}, ctx)
        if not upcoming_releases_data:
            return "Unable to fetch upcoming releases data."
        return json.dumps(paginated_response(upcoming_releases_data, start, len(upcoming_releases_data)), indent=4)


    @mcp.tool()
    async def get_country_codes_for_upcoming_releases(ctx: Context) -> str:
        """Get the available country codes for upcoming releases from IMDb.
        Returns:
            JSON object containing the available country codes for upcoming releases.
        """
        available_country_codes_url = f"{BASE_URL}/upcoming-releases-country-codes"
        available_country_codes_data = await make_imdb_request(available_country_codes_url, {}, ctx)
        if not available_country_codes_data:
            return "Unable to fetch available country codes for upcoming releases data."
        return json.dumps(available_country_codes_data, indent=4)


    # -----------------------------INDIA SPOTLIGHT TOOLS-----------------------------------

    @mcp.tool()
    async def get_top_rated_malayalam_movies(start: int, ctx: Context) -> str:
        """Top 50 Malayalam movies as rated by the IMDb users.
        Args:
            start: The starting index (0-based) to retrieve movies from.
        Returns:
            JSON object containing 5 top rated Malayalam movies starting from the specified index.
        """
        top_rated_malayalam_movies_url = f"{BASE_URL}/india/top-rated-malayalam-movies"
        top_rated_malayalam_movies_data = await make_imdb_request(top_rated_malayalam_movies_url, {}, ctx)
        if not top_rated_malayalam_movies_data:
            return "Unable to fetch top rated Malayalam movies data."
        
        # Use paginated response helper with fixed page size
        movies = top_rated_malayalam_movies_data.get("items", [])
        return json.dumps(paginated_response(movies, start, len(movies)), indent=4)


    @mcp.tool()
    async def get_upcoming_indian_movies(start: int, ctx: Context) -> str:
        """Get the most anticipated Indian movies on IMDb based on real-time popularity.
        Args:
            start: The starting index (0-based) to retrieve movies from.
        Returns:
            JSON object containing 5 most anticipated Indian movies starting from the specified index.
        """
        upcoming_indian_movies_url = f"{BASE_URL}/india/upcoming"
        upcoming_indian_movies_data = await make_imdb_request(upcoming_indian_movies_url, {}, ctx)
        if not upcoming_indian_movies_data:
            return "Unable to fetch upcoming Indian movies data."
        return json.dumps(paginated_response(upcoming_indian_movies_data, start, len(upcoming_indian_movies_data)), indent=4)


    @mcp.tool()
    async def get_trending_tamil_movies(start: int, ctx: Context) -> str:
        """Get the trending Tamil movies on IMDb.
        Args:
            start: The starting index (0-based) to retrieve movies from.
        Returns:
            JSON object containing 5 trending Tamil movies starting from the specified index.
        """
        trending_tamil_movies_url = f"{BASE_URL}/india/trending-tamil"
        trending_tamil_movies_data = await make_imdb_request(trending_tamil_movies_url, {}, ctx)
        if not trending_tamil_movies_data:
            return "Unable to fetch trending Tamil movies data."
        return json.dumps(paginated_response(trending_tamil_movies_data, start, len(trending_tamil_movies_data)), indent=4)


    @mcp.tool()
    async def get_trending_telugu_movies(start: int, ctx: Context) -> str:
        """Get the trending Telugu movies on IMDb.
        Args:
            start: The starting index (0-based) to retrieve movies from.
        Returns:
            JSON object containing 5 trending Telugu movies starting from the specified index.
        """
        trending_telugu_movies_url = f"{BASE_URL}/india/trending-telugu"
        trending_telugu_movies_data = await make_imdb_request(trending_telugu_movies_url, {}, ctx)
        if not trending_telugu_movies_data:
            return "Unable to fetch trending Telugu movies data."
        return json.dumps(paginated_response(trending_telugu_movies_data, start, len(trending_telugu_movies_data)), indent=4)


    @mcp.tool()
    async def get_top_rated_tamil_movies(start: int, ctx: Context) -> str:
        """Top 50 rated Tamil movies on IMDb.
        Args:
            start: The starting index (0-based) to retrieve movies from.
        Returns:
            JSON object containing 5 top rated Tamil movies starting from the specified index.
        """
        top_rated_tamil_movies_url = f"{BASE_URL}/india/top-rated-tamil-movies"
        top_rated_tamil_movies_data = await make_imdb_request(top_rated_tamil_movies_url, {}, ctx)
        if not top_rated_tamil_movies_data:
            return "Unable to fetch top rated Tamil movies data."
        return json.dumps(paginated_response(top_rated_tamil_movies_data, start, len(top_rated_tamil_movies_data)), indent=4)


    @mcp.tool()
    async def get_top_rated_telugu_movies(start: int, ctx: Context) -> str:
        """Top 50 rated Telugu movies on IMDb.
        Args:
            start: The starting index (0-based) to retrieve movies from.
        Returns:
            JSON object containing 5 top rated Telugu movies starting from the specified index.
        """
        top_rated_telugu_movies_url = f"{BASE_URL}/india/top-rated-telugu-movies"
        top_rated_telugu_movies_data = await make_imdb_request(top_rated_telugu_movies_url, {}, ctx)
        if not top_rated_telugu_movies_data:
            return "Unable to fetch top rated Telugu movies data."
        return json.dumps(paginated_response(top_rated_telugu_movies_data, start, len(top_rated_telugu_movies_data)), indent=4)


    @mcp.tool()
    async def get_top_rated_indian_movies(start: int, ctx: Context) -> str:
        """Top 250 rated Indian movies on IMDb with pagination.
        Args:
            start: The starting index (0-based) to retrieve movies from.
        Returns:
            JSON object containing 5 top rated Indian movies starting from the specified index.
        """
        top_rated_indian_movies_url = f"{BASE_URL}/india/top-rated-indian-movies"
        top_rated_indian_movies_data = await make_imdb_request(top_rated_indian_movies_url, {}, ctx)
        if not top_rated_indian_movies_data:
            return "Unable to fetch top rated Indian movies data."
        return json.dumps(paginated_response(top_rated_indian_movies_data, start, len(top_rated_indian_movies_data)), indent=4)
