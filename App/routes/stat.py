from imports import *

@app.route('/stat')
@login_required
def stat_page():
    df = pd.DataFrame(Candidacy.query.join(Users).with_entities(Users.first_name,Users.last_name,Users.email_address,Candidacy.status, Candidacy.entreprise).all(),columns=["first_name","last_name","mail","status","enterprise"])
    df["full_name"] = df["first_name"] + " " + df["last_name"]
    df["alternance"] = False
    df["alternance"].loc[df["status"]=="Alternance"] = True
    fig1 = px.histogram(df["full_name"])
    graphJSON1 = js.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    fig2 = px.pie(df[["mail","alternance"]].groupby(["mail"]).sum(),names="alternance")
    graphJSON2 = js.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('stat.html',graph1=graphJSON1, graph2=graphJSON2)