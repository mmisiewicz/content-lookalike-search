""" 
Main streamlit app 
"""

import logging
import os
import time

import psycopg
import streamlit as st
from psycopg.rows import dict_row
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
from typedef import Lookalike
from yarl import URL

install(show_locals=True)

LOG_FORMAT = "%(message)s"
CONSOLE = Console()
logging.basicConfig(
    level="INFO", format=LOG_FORMAT, datefmt="[%X] ", handlers=[RichHandler(rich_tracebacks=True, console=CONSOLE)]
)
LOGGER = logging.getLogger(__name__)


# Configure page layout
st.set_page_config(layout="wide")

# Title for the app
st.title("URL lookalike search tool")

# TODO: this address might flap due to dhcp, neet to set static lease. Also move
# it to 10G ethernet.
TRASCHAN = "10.200.0.131"


# Database connection function
# TODO: connection pool
def __get_db_connection() -> psycopg.Connection:
    """utility function to grab a DB connection"""

    LOGGER.debug("Getting DB connection")

    conn_params = {
        "host": TRASCHAN,
        "dbname": "mctxl",
        "user": os.getenv("USER"),
        "password": os.getenv("PGPASS"),
        "port": "5432",
    }
    return psycopg.connect(**conn_params)  # type: ignore


def __scrape_page():
    # TODO
    raise NotImplementedError


def __embed_text():
    # TODO
    raise NotImplementedError


def search_for_lookalikes(url: URL) -> list[Lookalike]:
    """
    Search the database for lookalies for `url`

    """
    # TODO: embed the texdt
    # TODO: keyword version
    res = []
    with __get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # TODO: write the hnsw query
            query = """
                SELECT id, url, bp_strings, 0.2 as distance, title, 
                published_time_eastern_date as published_date
                FROM rss_scraped_links
                WHERE domain = %s
                limit 100
            """
            cur.execute(query, (url.host,))
            rows = cur.fetchall()

            for row in rows:
                if row["title"] is not None:
                    title_str = row["title"] if len(row["title"]) <= 32 else row["title"][:32] + "..."
                else:
                    title_str = "none"

                res.append(
                    Lookalike(
                        neighbor_url=row["url"],
                        distance=row["distance"],
                        title=title_str,
                        id=row["id"],
                        published_date=row["published_date"],
                    )
                )

    return res


#### Below here, the app

url_input = st.text_input(
    "Enter URL(s) to search for lookalikes:",
    placeholder="https://example.com",
    value="https://www.nytimes.com/athletic/uk/",
)

# Create two columns for layout
# col1, col2 = st.columns(2)
(col1,) = st.columns(1)

# Main content in the first column
with col1:
    st.header("Query Results")

    # Query button
    if st.button("Run Query"):

        # true when clicked
        if url_input:

            # run the search, handle invalid input
            try:
                search_url = URL(url_input)
            except ValueError as e:
                LOGGER.debug("got invalid input [ %s ]", url_input)
                st.error("Invalid URL, try again fool")

            # create a spinner for better UX
            with st.spinner("Running query..."):
                # Add a small delay to make the spinner visible
                time.sleep(0.5)
                # Run the query
                results = search_for_lookalikes(search_url)

                if len(results) == 0:
                    st.warning("No results found for this URL.")

                st.table(results[:25])
                st.write("Found", len(results), "results")

        # true when input box is empty
        else:
            st.warning("Please enter a URL to query.")

# TODO:
# # Second column for future chart
# with col2:
#     st.header("Visualization")
#     st.info("TODO: create a visualization of the results here")

# Optional: Add some styling
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
    }
    table {
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
