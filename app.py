from flask import Flask,render_template,request
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import Setup
import seaborn as sns   

data = pd.read_csv('C:\\Users\\Manya Sharma\\Desktop\\data science flask\\Account Statements\\Ghodke-Aditya-Rao.csv')

app=Flask(__name__)

@app.route('/')
def index():
    categories, rec_alias, alias, alias_cat = Setup.setup()
    rec_list = []
    # data = pd.read_csv('C:\\Users\\Manya Sharma\\Desktop\\data science flask\\Account Statements\\Ghodke-Aditya-Rao.csv')
    global data
    dd = list(data['Description'])
    
    for rec in dd:
        # print(rec)
        try:
            rec = rec.split('/')
            if rec[0] == 'UPI':
                try:
                    # print(rec[4])0
                    rec_list.append(rec[4].split('@')[0])
                except:
                    rec_list.append("Other")
            else:
                rec_list.append("Other")
        except:
            rec_list.append("Other")
    
    categories, rec_alias, alias, alias_cat = Setup.run(rec_list, categories, rec_alias, alias, alias_cat)

    data['Category'] = list(map(lambda x: alias_cat[rec_alias[x]], rec_list))
    data = data.replace({'Credit': 1, 'Debit': -1})
    data['Amount'] = data['Amount'] * data['Type']

    category_seg = data.groupby(['Category', 'Date']).agg('sum')['Amount']
    category_tot = data.groupby(['Category']).agg('sum')['Amount']
    month = []
    for date in data['Date']:
        month.append(date.split('/')[0])
    data['Month'] = month
    category_month = data.groupby(['Category', 'Month']).agg('sum')['Amount']

    Setup.finishRun(categories, rec_alias, alias, alias_cat)

    #pie plot
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    category_tot = category_tot.to_dict()
    labels = []
    values = []
    for key in category_tot:
        if category_tot[key] < 0:
            values.append(-category_tot[key])
            labels.append(key)
    plt.pie(list(values),
            explode=[0.1]*len(labels), shadow="True",autopct='%1.0f%%')

    plt.legend(labels=labels, loc="upper left", bbox_to_anchor=(1, 1))
    # fig = plt.figure(figsize = (10, 5))
    plt.plot()
    plt.savefig('static//my_pie.png')


    return render_template("dispaly.html", data = category_tot)

    
    
    
    # return (render_template('dispaly.html',food_per=dic.food,online_per=y,travel_per=z))


@app.route('/transaction')
def transaction():
    return render_template("index.html")

@app.route('/plot')
def plot():
    data = {'C':20, 'C++':15, 'Java':30,
        'Python':35}
    courses = list(data.keys())
    values = list(data.values())
    
    fig = plt.figure(figsize = (10, 5))
    

    plt.bar(courses, values, color ='maroon',
            width = 0.4)
    fig.savefig('static/my_plot.png')
    return render_template("pie.html")


@app.route('/test')
def tests():
    return render_template('test.html')

# @app.route('/test_data',methods=['POST'])
# def test():
#     global data
#     cats = request.form.getlist('category')
#     # print(cats)
    
#     cat_group = data[data["Category"].isin(cats)].groupby(["Category", "Date"], sort=False).agg('sum')['Amount'].to_frame()
#     fig, ax = plt.subplots()
#     sns.lineplot(data=cat_group, x="Date", y="Amount", hue="Category", ax=ax)
#     # sns.lmplot(x="Date", y="Amount", data=cat_group, hue="Category")
#     fig.legend(labels=cats)
#     # fig.xticks(rotation=90)
#     # a.show()
#     fig.savefig("static//my_expense.png")
#     return render_template("test.html",msg="done")

if __name__=="__main__":
    app.run(debug=True)