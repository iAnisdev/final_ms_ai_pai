
import cufflinks as cf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
from shiny.ui import output_ui
from shinywidgets import render_plotly
from db import get_connection

# Initialize the database pool asynchronously
db_pool = None


async def initialize_db():
    global db_pool
    db_pool = await get_connection()


@reactive.Effect
async def app_startup():
    await initialize_db()


# Default to the last 1 year
end = pd.Timestamp.now() - pd.Timedelta(days=1)
start = end - pd.Timedelta(weeks=52)
# 5 years back
min = end - pd.Timedelta(weeks=52 * 5)
max = pd.Timestamp.now()


ui.page_opts(title="Multi-Crypto Price Analysis", fillable=True)

with ui.sidebar():
    ui.input_selectize(
        "ticker",
        "Select Crypto",
        choices=list(
            {
                "Bitcoin": "bitcoin",
                "Ethereum": "ethereum",
                "Binance": "binance",
                "Solana": "solana",
            }
        ),
        selected="Bitcoin",
    )
    ui.input_date_range("dates", "Select dates", start=start, end=end, min=min, max=max)
    ui.input_radio_buttons(  
        "predict",
        "Predict Price",
        {1: "1 Day", 3: "3 Days", 7: "1 Week", 30: "1 Month"},
    )


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("dollar-sign")):
        "Current Price"

        @render.ui
        async def price():
            # Get the latest timestamp col price of the selected ticker from the database using
            last = await get_end_price()
            end_price = last.get("close")
            return f"${end_price:.2f}" if end_price else "N/A"

    with ui.value_box(showcase=output_ui("change_icon")):
        "Expected Change"

        @render.ui
        async def change():
            resp = await get_predicted_price()
            price = resp.get("price")
            return f"${price:.2f}" if price else "N/A"

    with ui.value_box(showcase=icon_svg("percent")):
        "Percent Change"

        @render.ui
        async def change_percent():
            resp = await get_predicted_price()
            change = resp.get("change")
            return f"{change:.6f}%" if change else "N/A"


with ui.layout_columns(col_widths=[9, 3]):
    with ui.card(full_screen=True):
        ui.card_header("Price history")

        @render_plotly
        async def price_history():
            data = await get_data()
            # Convert result to pandas DataFrame
            data = pd.DataFrame([dict(row) for row in data])
            data.set_index("timestamp", inplace=True)  # Set timestamp as index
        
            qf = cf.QuantFig(
                data,
                name=input.ticker(),
                up_color="#44bb70",
                down_color="#040548",
                legend="top",
            )
            qf.add_sma()
            fig = qf.figure()
            fig.update_layout(
                hovermode="x unified",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            return fig

    with ui.card():
        ui.card_header("Latest data")

        @render.data_frame
        async def latest_data():
            data = await get_end_price()
            x = pd.DataFrame(
                [
                    {"Category": "Open", "Value": f"${data.get('open'):.2f}"},
                    {"Category": "High", "Value": f"${data.get('high'):.2f}"},
                    {"Category": "Low", "Value": f"${data.get('low'):.2f}"},
                    {"Category": "Close", "Value": f"${data.get('close'):.2f}"},
                    {"Category": "Volume", "Value": f"{data.get('volume'):.2f}"},
                    {
                        "Category": "Number of Trades",
                        "Value": f"{data.get('number_of_trades'):.0f}",
                    },
                ]
            )
            return x
        
        @render.plot
        def hist():
            df = pd.DataFrame(data=[
                {"date": "2024-12-29", "predicted_value": 30000},
                {"date": "2024-12-30", "predicted_value": 30500},
                {"date": "2024-12-31", "predicted_value": 31000},
                {"date": "2025-01-01", "predicted_value": 32000},
                {"date": "2025-01-02", "predicted_value": 31500},
                {"date": "2025-01-03", "predicted_value": 33000},
                {"date": "2025-01-04", "predicted_value": 34000},
            ], columns=["date", "predicted_value"])

            plt.figure(figsize=(10, 6))
            sns.lineplot(data=df, x="date", y="predicted_value", marker="o", label="Predicted BTC Value")

            value = input.predict()
            plt.title(f"Predicted Value for Next {value} Days")
            plt.xlabel("Date")
            plt.ylabel("Predicted Value")
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
            plt.legend()
            plt.grid(True)

with ui.layout_columns(col_widths=[12]):
    with ui.card(full_screen=True):
            ui.card_header("Volume history")
            @render_plotly
            async def render_volume():
                data = await get_data()
                # Convert result to pandas DataFrame and with only the volume and timestamp columns
                data = pd.DataFrame([dict(row) for row in data])
                data = data[["volume", "timestamp"]]
                fig = px.line(
                    data,
                    x="timestamp",
                    y="volume",
                    title=f"Volume of {input.ticker()} over time",
                    labels={"timestamp": "Timestamp", "volume": "Volume"},
                )

                fig.update_layout(
                    xaxis_title="Timestamp",
                    yaxis_title="Volume"
                )

                return fig

@reactive.calc
def get_ticker():
    return input.ticker()


@reactive.calc
async def get_data():
    """
    Reactive function to fetch data for the selected table  input.ticker() .
    """
    ticker = input.ticker().lower()
    query = f"SELECT * FROM {ticker}"  # Safely interpolate the table name (if safe)

    async with db_pool.acquire() as connection:
        result = await connection.fetch(query)
        return result
    


@reactive.calc
async def get_end_price():
    ticker = input.ticker().lower()
    query = f"SELECT * FROM {ticker} ORDER BY timestamp DESC LIMIT 1"

    async with db_pool.acquire() as connection:
        result = await connection.fetch(query)
        return result[0]


@reactive.calc
async def get_predicted_price():
    data = await get_end_price()
    return {
        "price": data.get("close") + 10,
        "change": 0.00001,
        "best_day": "2021-10-10",
    }
with ui.hold():

    @render.ui
    async def change_icon():
        resp = await get_predicted_price()
        change = resp.get("change")
        icon = icon_svg("arrow-up" if change >= 0 else "arrow-down")
        icon.add_class(f"text-{('success' if change >= 0 else 'danger')}")
        return icon

# add css files
ui.include_css("./styles/light.css")
ui.include_css("./styles/dark.css")