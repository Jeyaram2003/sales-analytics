from flask import Flask, render_template, request, redirect, flash, session, send_file
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = "salesanalytics"
app.jinja_env.globals.update(zip=zip)

# ── Paths (work on both local and Render) ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_PATH = os.path.join(BASE_DIR, "uploads", "sales_data.xlsx")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "uploads"), exist_ok=True)

# ── Helper: load and prepare dataframe ──
def load_df():
    df = pd.read_excel(UPLOAD_PATH)
    df['SalesDate'] = pd.to_datetime(df['SalesDate'])
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    return df

# ── Helper: train ML model ──
def train_model(df):
    ml_df = df.copy()
    le_product  = LabelEncoder()
    le_category = LabelEncoder()
    le_region   = LabelEncoder()
    ml_df['Product']  = le_product.fit_transform(ml_df['Product'])
    ml_df['Category'] = le_category.fit_transform(ml_df['Category'])
    ml_df['Region']   = le_region.fit_transform(ml_df['Region'])
    X = ml_df[['Product','Category','Quantity','UnitPrice','Region']]
    y = ml_df['Revenue']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae  = round(mean_absolute_error(y_test, y_pred), 2)
    rmse = round(np.sqrt(mean_squared_error(y_test, y_pred)), 2)
    r2   = round(r2_score(y_test, y_pred), 4)
    return model, ml_df, mae, rmse, r2

# =============================================
# HOME — Landing Page
# =============================================
@app.route('/')
def home():
    return render_template('index.html')

# =============================================
# LOGIN
# =============================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "admin123":
            session['user'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid Username or Password")
    return render_template('login.html')

# =============================================
# LOGOUT
# =============================================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# =============================================
# DASHBOARD
# =============================================
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    df = load_df()
    total_revenue = round(df['Revenue'].sum(), 2)
    total_orders  = len(df)
    top_product   = df.groupby('Product')['Revenue'].sum().idxmax()
    best_region   = df.groupby('Region')['Revenue'].sum().idxmax()
    region_sales  = df.groupby('Region')['Revenue'].sum().reset_index()
    region_labels = region_sales['Region'].tolist()
    region_values = region_sales['Revenue'].tolist()
    product_sales  = df.groupby('Product')['Revenue'].sum().reset_index()
    product_labels = product_sales['Product'].tolist()
    product_values = product_sales['Revenue'].tolist()
    df['Month']    = df['SalesDate'].dt.strftime('%b')
    monthly_sales  = df.groupby('Month')['Revenue'].sum().reset_index()
    month_labels   = monthly_sales['Month'].tolist()
    month_values   = monthly_sales['Revenue'].tolist()
    _, _, mae, rmse, r2 = train_model(df)
    return render_template("dashboard.html",
        total_revenue=total_revenue, total_orders=total_orders,
        top_product=top_product, best_region=best_region,
        region_labels=region_labels, region_values=region_values,
        product_labels=product_labels, product_values=product_values,
        month_labels=month_labels, month_values=month_values,
        mae=mae, rmse=rmse, r2=r2)

# =============================================
# REVENUE
# =============================================
@app.route('/revenue')
def revenue():
    if 'user' not in session:
        return redirect('/login')
    df = load_df()
    total_revenue   = round(df['Revenue'].sum(), 2)
    average_revenue = round(df['Revenue'].mean(), 2)
    df['Month']     = df['SalesDate'].dt.strftime('%b')
    monthly_sales   = df.groupby('Month')['Revenue'].sum().reset_index()
    month_labels    = monthly_sales['Month'].tolist()
    month_values    = monthly_sales['Revenue'].tolist()
    best_month      = monthly_sales.loc[monthly_sales['Revenue'].idxmax(), 'Month']
    return render_template('revenue.html',
        total_revenue=total_revenue, average_revenue=average_revenue,
        best_month=best_month, month_labels=month_labels, month_values=month_values)

# =============================================
# PRODUCT
# =============================================
@app.route('/product')
def product():
    if 'user' not in session:
        return redirect('/login')
    df = load_df()
    product_sales       = df.groupby('Product')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False)
    top_product         = product_sales.iloc[0]['Product']
    top_product_revenue = round(product_sales.iloc[0]['Revenue'], 2)
    total_products      = product_sales['Product'].nunique()
    product_labels      = product_sales['Product'].tolist()
    product_values      = product_sales['Revenue'].tolist()
    product_table       = product_sales.to_dict('records')
    return render_template('product.html',
        top_product=top_product, top_product_revenue=top_product_revenue,
        total_products=total_products, product_labels=product_labels,
        product_values=product_values, product_table=product_table)

# =============================================
# REGION
# =============================================
@app.route('/region')
def region():
    if 'user' not in session:
        return redirect('/login')
    df = load_df()
    region_sales       = df.groupby('Region')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False)
    best_region        = region_sales.iloc[0]['Region']
    best_region_revenue= round(region_sales.iloc[0]['Revenue'], 2)
    total_regions      = region_sales['Region'].nunique()
    region_labels      = region_sales['Region'].tolist()
    region_values      = region_sales['Revenue'].tolist()
    return render_template('region.html',
        best_region=best_region, best_region_revenue=best_region_revenue,
        total_regions=total_regions, region_labels=region_labels, region_values=region_values)

# =============================================
# PREDICTION
# =============================================
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if 'user' not in session:
        return redirect('/login')
    df = load_df()
    model, ml_df, mae, rmse, r2 = train_model(df)
    prediction_result = None
    month = None
    if request.method == 'POST':
        month = int(request.form['month'])
        avg_product    = ml_df['Product'].mean()
        avg_category   = ml_df['Category'].mean()
        avg_quantity   = df['Quantity'].mean()
        avg_unit_price = df['UnitPrice'].mean()
        avg_region     = ml_df['Region'].mean()
        prediction_result = round(
            model.predict([[avg_product, avg_category, avg_quantity, avg_unit_price, avg_region]])[0] * (month / 6), 2)
    return render_template('prediction.html',
        mae=mae, rmse=rmse, r2=r2,
        prediction=prediction_result, month=month)

# =============================================
# FORECAST
# =============================================
@app.route('/forecast')
def forecast():
    if 'user' not in session:
        return redirect('/login')
    df = load_df()
    df['MonthNum']  = df['SalesDate'].dt.month
    monthly_sales   = df.groupby('MonthNum')['Revenue'].sum().reset_index()
    X = monthly_sales[['MonthNum']]
    y = monthly_sales['Revenue']
    model = LinearRegression()
    model.fit(X, y)
    future_months  = [int(monthly_sales['MonthNum'].max()) + i for i in range(1, 4)]
    future_revenue = [round(float(model.predict([[m]])[0]), 2) for m in future_months]
    hist_labels    = monthly_sales['MonthNum'].astype(str).tolist()
    hist_values    = [round(float(v), 2) for v in monthly_sales['Revenue'].tolist()]
    fore_labels    = [str(m) for m in future_months]
    fore_values    = future_revenue
    return render_template("forecast.html",
        hist_labels=hist_labels, hist_values=hist_values,
        fore_labels=fore_labels, fore_values=fore_values,
        future_month=future_months[0], predicted_revenue=future_revenue[0])

# =============================================
# REPORTS
# =============================================
@app.route('/reports')
def reports():
    if 'user' not in session:
        return redirect('/login')
    df = load_df()
    total_revenue = round(df['Revenue'].sum(), 2)
    total_orders  = len(df)
    top_product   = df.groupby('Product')['Revenue'].sum().idxmax()
    best_region   = df.groupby('Region')['Revenue'].sum().idxmax()
    _, _, mae, rmse, r2 = train_model(df)
    return render_template('reports.html',
        total_revenue=total_revenue, total_orders=total_orders,
        top_product=top_product, best_region=best_region,
        mae=mae, rmse=rmse, r2=r2)

# =============================================
# DOWNLOAD REPORT
# =============================================
@app.route('/download_report')
def download_report():
    if 'user' not in session:
        return redirect('/login')
    df = load_df()
    total_revenue = round(df['Revenue'].sum(), 2)
    total_orders  = len(df)
    top_product   = df.groupby('Product')['Revenue'].sum().idxmax()
    best_region   = df.groupby('Region')['Revenue'].sum().idxmax()
    pdf_path = os.path.join(REPORTS_DIR, "Sales_Report.pdf")
    doc      = SimpleDocTemplate(pdf_path)
    styles   = getSampleStyleSheet()
    content  = []
    content.append(Paragraph("Sales Analytics Report", styles['Title']))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Total Revenue: Rs.{total_revenue}", styles['BodyText']))
    content.append(Paragraph(f"Total Orders: {total_orders}",      styles['BodyText']))
    content.append(Paragraph(f"Top Product: {top_product}",        styles['BodyText']))
    content.append(Paragraph(f"Best Region: {best_region}",        styles['BodyText']))
    doc.build(content)
    return send_file(pdf_path, as_attachment=True)

# =============================================
# UPLOAD
# =============================================
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(UPLOAD_PATH)
            flash("Dataset uploaded successfully!")
            return redirect("/upload")
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)
