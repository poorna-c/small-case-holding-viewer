# import plotly.express as px

# def generate_timeline_chart(df):
#     df = df.sort_values("Holding Weeks", ascending=False)

#     fig = px.timeline(
#         df,
#         x_start="Entry",
#         x_end="Exit",
#         y="Stock",
#         color="Stock",
#         hover_data=["Holding Weeks"],
#         template="plotly_white"
#     )

#     fig.update_layout(
#         title="Smallcase Portfolio Holding Timeline",
#         xaxis_title="Time",
#         yaxis_title="Stocks",
#         showlegend=False,
#         height=900
#     )

#     fig.update_yaxes(autorange="reversed")

#     return fig.to_html(full_html=False)


# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import pandas as pd

# def generate_dashboard(df):

#     # ===== Summary Calculations =====
#     total_stocks = df['Stock'].nunique()
#     total_periods = len(df)
#     avg_holding = round(df['Holding Weeks'].mean(), 2)

#     summary = df.groupby('Stock')['Holding Weeks'].sum().reset_index()
#     summary = summary.sort_values("Holding Weeks", ascending=False)

#     top_stock = summary.iloc[0]['Stock']
#     top_stock_duration = round(summary.iloc[0]['Holding Weeks'], 2)

#     # ===== Bar Chart for Total Holding Time =====
#     bar_fig = px.bar(
#         summary,
#         x="Holding Weeks",
#         y="Stock",
#         orientation="h",
#         title="Total Holding Duration per Stock (Weeks)",
#         template="plotly_white"
#     )

#     bar_fig.update_layout(height=800)
#     bar_fig.update_yaxes(autorange="reversed")

#     # ===== Convert DataFrame to HTML Table =====
#     table_html = df.sort_values("Entry").to_html(
#         index=False,
#         classes="table table-striped",
#         border=0
#     )

#     # ===== Final HTML Page =====
#     html_content = f"""
#     <html>
#     <head>
#         <title>Smallcase Portfolio Dashboard</title>
#         <style>
#             body {{
#                 font-family: Arial;
#                 margin: 40px;
#                 background-color: #f4f6f9;
#             }}
#             .card-container {{
#                 display: flex;
#                 gap: 20px;
#                 margin-bottom: 30px;
#             }}
#             .card {{
#                 background: white;
#                 padding: 20px;
#                 border-radius: 10px;
#                 box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#                 flex: 1;
#                 text-align: center;
#             }}
#             h1 {{
#                 margin-bottom: 30px;
#             }}
#             table {{
#                 background: white;
#                 width: 100%;
#                 border-collapse: collapse;
#             }}
#             th, td {{
#                 padding: 8px;
#                 text-align: left;
#                 border-bottom: 1px solid #ddd;
#             }}
#             th {{
#                 background-color: #2c3e50;
#                 color: white;
#             }}
#         </style>
#     </head>
#     <body>

#     <h1>Smallcase Portfolio Holdings Dashboard</h1>

#     <div class="card-container">
#         <div class="card">
#             <h2>{total_stocks}</h2>
#             <p>Total Unique Stocks</p>
#         </div>
#         <div class="card">
#             <h2>{total_periods}</h2>
#             <p>Total Holding Periods</p>
#         </div>
#         <div class="card">
#             <h2>{avg_holding}</h2>
#             <p>Average Holding (Weeks)</p>
#         </div>
#         <div class="card">
#             <h2>{top_stock}</h2>
#             <p>Longest Held ({top_stock_duration} Weeks)</p>
#         </div>
#     </div>

#     <div>
#         {bar_fig.to_html(full_html=False)}
#     </div>

#     <h2>All Entry-Exit Records</h2>

#     {table_html}

#     </body>
#     </html>
#     """

#     return html_content



import plotly.express as px
import pandas as pd

def generate_dashboard(df):

    total_stocks = df['Stock'].nunique()
    total_periods = len(df)
    avg_holding = round(df['Holding Weeks'].mean(), 2)

    summary = df.groupby('Stock')['Holding Weeks'].sum().reset_index()
    summary = summary.sort_values("Holding Weeks", ascending=False)

    top_stock = summary.iloc[0]['Stock']
    top_stock_duration = round(summary.iloc[0]['Holding Weeks'], 2)

    bar_fig = px.bar(
        summary,
        x="Holding Weeks",
        y="Stock",
        orientation="h",
        template="plotly_white"
    )

    bar_fig.update_layout(height=700)
    bar_fig.update_yaxes(autorange="reversed")

    table_html = df.sort_values("Entry").to_html(
        index=False,
        classes="table table-hover table-bordered",
        border=0
    )

    return f"""
    <div class="container mt-5">

        <div class="row text-center mb-4">
            <div class="col-md-3">
                <div class="card p-3">
                    <h5>Total Stocks</h5>
                    <h3>{total_stocks}</h3>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-3">
                    <h5>Total Holding Periods</h5>
                    <h3>{total_periods}</h3>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-3">
                    <h5>Avg Holding (Weeks)</h5>
                    <h3>{avg_holding}</h3>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-3">
                    <h5>Longest Held</h5>
                    <h6>{top_stock}</h6>
                    <small>{top_stock_duration} Weeks</small>
                </div>
            </div>
        </div>

        <div class="card p-4 mb-5">
            <h5 class="mb-4">Total Holding Duration per Stock</h5>
            {bar_fig.to_html(full_html=False)}
        </div>

        <div class="card p-4">
            <h5 class="mb-3">All Entry-Exit Records</h5>

            <input type="text" id="stockSearch" 
                   class="form-control mb-3" 
                   placeholder="Search stock name..."
                   onkeyup="filterTable()">

            <div class="table-responsive">
                {table_html.replace('<table', '<table id="holdingTable"')}
            </div>
        </div>

    </div>

    <script>
    function filterTable() {{
        let input = document.getElementById("stockSearch");
        let filter = input.value.toLowerCase();
        let table = document.getElementById("holdingTable");
        let tr = table.getElementsByTagName("tr");

        for (let i = 1; i < tr.length; i++) {{
            let td = tr[i].getElementsByTagName("td")[0];
            if (td) {{
                let txtValue = td.textContent || td.innerText;
                tr[i].style.display = txtValue.toLowerCase().includes(filter) ? "" : "none";
            }}
        }}
    }}
    </script>
    """


def generate_timeline_chart(df):
    fig = px.timeline(
        df,
        x_start="Entry",
        x_end="Exit",
        y="Stock",
        color="Stock",
        template="plotly_white"
    )

    fig.update_layout(height=800, showlegend=False)
    fig.update_yaxes(autorange="reversed")

    return fig.to_html(full_html=False)
