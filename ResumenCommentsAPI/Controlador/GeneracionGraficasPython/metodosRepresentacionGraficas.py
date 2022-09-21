from cmath import log
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import iplot
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd


def nubePalabras(data,filename):
    ##Pasamos nuestra columna a texto
    text = " ".join(review for review in data)
    ##Definicion 
    wc = WordCloud(max_words=40,width=848, height=480,background_color="white", colormap="Dark2", max_font_size=150, random_state=42)
    wordcloud = wc.generate(text)
    wordcloud.to_file("static/images/nubePalabras/"+filename+'.png')
    return "static/images/nubePalabras/"+filename+'.png'

def usuariosByGenero(data):
    df = data
    top_labels = ['Hombres', 'Mujeres', 'lgbtiq+']

    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
            'rgba(122, 120, 168, 0.8)']

    try:
        cantidadHombres = (df["genero"].value_counts())['Hombres']
    except:
        cantidadHombres = 0

    try:
        cantidadMujeres = (df["genero"].value_counts())['Mujeres']
    except:
        cantidadMujeres = 0

    try:
        cantidadLGBT = (df["genero"].value_counts())['lgbtiq+']
    except:
        cantidadLGBT = 0
    total = cantidadHombres+cantidadMujeres+cantidadLGBT 
    x_data = [[int((cantidadHombres/total)*100), int((cantidadMujeres/total)*100), int((cantidadLGBT/total)*100)]]
    y_data = ['Genero']

    fig = go.Figure()
    cont = 0
    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                ),
                name=top_labels[cont]
            ))
            cont = cont + 1 
    
    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=30, r=30, t=100, b=100),
        showlegend=True,
        height=400
    )

    annotations = []

    for yd, xd in zip(y_data, x_data):
        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',
                                x=xd[0] / 2, y=yd,
                                text=str(xd[0]) + '%',
                                font=dict(family='Arial', size=15,
                                        color='rgb(248, 248, 255)'),
                                showarrow=False))
       
        space = xd[0]
        for i in range(1, len(xd)):
                # labeling the rest of percentages for each bar (x_axis)
                annotations.append(dict(xref='x', yref='y',
                                        x=space + (xd[i]/2), y=yd,
                                        text=str(xd[i]) + '%',
                                        font=dict(family='Arial', size=15,
                                                color='rgb(248, 248, 255)'),
                                        showarrow=False))
                space += xd[i]

    fig.update_layout(annotations=annotations)
    fig.write_image("static/images/genero/generoUsers.png",format='png',engine='kaleido',scale=2)
    return "static/images/genero/generoUsers.png"


def graficaDeSentimientoComentario(data):
    df = data
    tipos = ['Muy Bueno', 'Bueno', 'Neutro', 'Malo', 'Muy Malo']
    try:
        muyBueno = (df["tipo_comentario"].value_counts())['very positive']
    except:
        muyBueno = 0
    try:
        bueno = (df["tipo_comentario"].value_counts())['positive']
    except:
        bueno = 0
    try:
        neutro = (df["tipo_comentario"].value_counts())['mixed']
    except:
        neutro = 0
    try:
        malo = (df["tipo_comentario"].value_counts())['negative']
    except:
        malo = 0
    try:
        muyMalo = (df["tipo_comentario"].value_counts())['very negative']
    except:
        muyMalo = 0

    fig = px.pie(values=[muyBueno, bueno, neutro, malo, muyMalo],names=tipos,
                color=tipos,
                color_discrete_map={'Muy Bueno':'#446AA3',
                                    'Bueno':'#DEE2FF',
                                    'Neutro':'#B3B9E8',
                                    'Malo':'#E8B3B7',
                                    'Muy Malo':'#9C595F'}
                )
    pathImg = "static/images/clasificacionSentimiento/sentimientoComentarioPie.png"
    fig.write_image(pathImg,format='png',engine='kaleido')
    
    return pathImg

def graficaPorEdades(data):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data['edad'],
        histfunc='count',
        marker_color='#809FC2',
        opacity=0.75,
        xbins=dict( # bins used for histogram
            start=0.0,
            end=100.0,
            size=5
        ),
    ))
    fig.update_layout(
        xaxis_title_text='Edad', # xaxis label
        yaxis_title_text='Numero de Personas', # yaxis label
        xaxis_range=[0,100],
        bargap=0.05, # gap between bars of adjacent location coordinates
        bargroupgap=0.05 # gap between bars of the same location coordinates
    )

    pathImg = "static/images/edades/edadesUsuarios.png"
    fig.write_image(pathImg,format='png',engine='kaleido')
    return pathImg



def vectorizacionPalabras(corpus, ngrama,n):
    vec = CountVectorizer(ngram_range=(ngrama, ngrama)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

def obtener_top_n_words(data, type, ngrama,n=10):
    common_words = vectorizacionPalabras(data[type], ngrama, n)
    df2 = pd.DataFrame(common_words, columns = [ type, 'count'])
    df2.groupby(type).sum()['count'].sort_values(ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="sum", y=df2['count'], x=df2[type], name="sum",marker_color='lightsalmon'))
    if(type == 'token_text'):
        pathImg = "static/images/ngramas/ugramasComentario.png"
    else: 
        pathImg = "static/images/ngramas/ugramasResumen.png"

    fig.write_image(pathImg,format='png',engine='kaleido')
    return pathImg