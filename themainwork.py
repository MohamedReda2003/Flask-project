
from flask import Flask,render_template,request,redirect,url_for

from pymongo import MongoClient
from playwright.sync_api import Playwright, sync_playwright, expect
import Levenshtein as lev
from random import randint

import datetime

app=Flask(__name__)

test=True

cluster=MongoClient("mongodb+srv://fiverrautomation:he3eyetR@cluster0.pshiyd4.mongodb.net/?retryWrites=true&w=majority")
db =cluster["locantoaccount"]
collection=db["locanto"]
user_details={}
user={}
image_number=0
@app.route('/', methods =["GET", "POST"])
def first():
    global image_number
    if request.method == "POST":
        image_number= request.form['image number']
        image_number=int(image_number)
        return redirect(url_for('start'))
    return """
            <form action="#" method="post" enctype="multipart/form-data">
                <div>
                    <label for imagenumber="numbers"><b>El número de imágenes que pretendes subir :</b></label>
                    <input type="number" name="image number">
                </div>
                <input type="submit" value="Submit">
            </form>
            """
        
        
    
    
@app.route('/register', methods =["GET", "POST"])
def start():
    global user_details
    if request.method == "POST":
        email=request.form['email']
        title=request.form['title']
        psw=request.form['psw']
        direction=request.form['direction']
        postal=request.form['Code postal']
        city=request.form['city'] 
        description=request.form['description']
        today = datetime.date.today()
        redoday = today + datetime.timedelta(days=42)
        today=str(today)
        redoday=str(redoday)
        
        try:
            phone_number=request.form['phone number']
        except :
            pass
        try:
            new_images=[]
            imagepath = request.form.getlist('image')
            alpha=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
            alpha2= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
            
            for image in imagepath:
                for i in range(len(alpha)):
                    image=image.replace(f'\{alpha[i]}',f'/{alpha[i]}').replace(f'\{alpha2[i]}',f'/{alpha2[i]}')
                new_images.append(image)
            imagepath=[]
            imagepath=new_images
                        
                    
            
            
        except : 
            pass
        try:
            website=request.form['website']
        except :
            pass
        qw=email+f'{randint(1,6)}'+f'{randint(7,15)}'+city+f'{randint(20,28)}'+title
        try:
            g=0
            qws=collection.find({'email': email,'password': psw})
            for naw in qws:
                if lev.ratio(naw['_id'],qw)>0.8:
                    g+=1
                    break
            if g !=0:
                user=naw
                today = datetime.date.today()
                second_date=user['redo date']
                second_date = datetime.datetime.strptime(second_date, '%Y-%m-%d').date()
                left=second_date-today
                if left==0:
                    return redirect(url_for('summon'))
                left=str(left)
                dayis=left[:2]
                return render_template('success.html', userwork=user, days=dayis)
                
        except:
            pass
            
        user_details.update({
            '_id':qw,
            'email': email,
            'password': psw,
            'title':title,
            'description':description,
            'city': city,
            'date':today,
            'redo date':redoday
        })

        try:
            if direction != "":
                user_details.update({'direction':direction})
        except :
            pass
        
        try:
            if postal !="":
                user_details.update({'code postal':postal})
        except:
            pass
        
        try:
            if phone_number !="":
                user_details.update({'phone number':phone_number})
        except :
            pass
        try:
            if website !="":
                user_details.update({'website':website})
        except :
            pass
        try:
            user_details.update({'image path':imagepath})
        except :
            pass
        data=collection.find(user_details)
        if len(list(data))==0:
            return redirect(url_for("cate")) 
            
        else:
            return "you are aleady in"
    return render_template('index.html',images=image_number)

    
@app.route('/go', methods =["GET", "POST"])
def cate ():
    if request.method == "POST":
        category=request.form['category']
        user_details.update({'category':category})
        categoria=category.replace(' / ','').replace('text=','')
        return redirect(url_for(f'sub{categoria}'))
    return render_template("category_and_subs.html")



@app.route('/Clases', methods =["GET", "POST"])
def subClases():
    
    if request.method == "POST":
        subcategory=request.form['subclase']
        startdate=request.form['startdate']
        enddate=request.form['enddate']
        user_details.update({'subcategory':subcategory})
        if startdate !="":
            user_details.update({'start date':startdate})
        if enddate !="":
            user_details.update({'end date':enddate})

        clasesub=subcategory.replace(',','').replace(' ','').replace('text=','')
        if  clasesub=='Artemúsicabaile':
            return redirect(url_for(f'{clasesub}'))
        elif clasesub=='Cursosdeinformática' :
            return redirect(url_for(f'{clasesub}'))
        else: 
            return redirect(url_for('finish'))
        
    
    return render_template('clases.html')


@app.route('/Cursosdeinformática', methods =["GET", "POST"])       
def Cursosdeinformática():
    
    if request.method=='POST':
        subsubcategory=request.form['subsubclase']
        user_details.update({'subsubcategory':subsubcategory})
        return redirect(url_for('finish'))
    return render_template('Cursosdeinformática.html')


@app.route('/Artemúsicabaile', methods =["GET", "POST"])
def Artemúsicabaile():
    
    if request.method=='POST':
        subsubcategory=request.form['subsubclase']
        user_details.update({'subsubcategory':subsubcategory})
        return redirect(url_for('finish'))
    
    return render_template('Arte_música_baile.html')




@app.route('/CompraVenta', methods =["GET", "POST"])
def subCompraVenta():

    if request.method == "POST":
        subcategory=request.form['subcompraventa']
        price=request.form['price']
        transmission=request.form['transmission']
        user_details.update({'subcategory':subcategory})
        try:
            user_details.update({'price':price})
        except :
            pass
        
        try:
            user_details.update({'transmission':transmission})
        except : 
            pass
            
        ventasub=subcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for(f'{ventasub}'))
    return render_template('CompraVenta.html')


@app.route('/Aficionesytiempolibre', methods =["GET", "POST"])
def Aficionesytiempolibre():
    if request.method == "POST":
        subsubcategory=request.form['subsubventa']
        user_details.update({'subsubcategory':subsubcategory})
        ventasub=subsubcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Aficionesytiempolibre.html')

@app.route('/Bebésyniños', methods =["GET", "POST"])
def Bebésyniños():
    if request.method == "POST":
        subsubcategory=request.form['subsubcompraventa']
        user_details.update({'subsubcategory':subsubcategory})
        ventasub=subsubcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Bebésyniños.html')

@app.route('/Bellezaymoda', methods =["GET", "POST"])
def Bellezaymoda():

    if request.method == "POST":
        subsubcategory=request.form['subsubcompraventa']
        user_details.update({'subsubcategory':subsubcategory})
        ventasub=subsubcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Bellezaymoda.html')


@app.route('/Hogaryjardín', methods =["GET", "POST"])
def Hogaryjardín():
    if request.method == "POST":
        subsubcategory=request.form['subsubventa']
        user_details.update({'subsubcategory':subsubcategory})
        ventasub=subsubcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Hogaryjardín.html')

@app.route('/Informáticaymultimedia', methods =["GET", "POST"])
def Informáticaymultimedia():
    if request.method == "POST":
        subsubcategory=request.form['subsubventa']
        user_details.update({'subsubcategory':subsubcategory})
        ventasub=subsubcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Informáticaymultimedia.html')

@app.route('/Músicacineylibros', methods =["GET", "POST"])
def Músicacineylibros():
    if request.method == "POST":
        subsubcategory=request.form['subsubventa']
        user_details.update({'subsubcategory':subsubcategory})
        ventasub=subsubcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Músicacineylibros.html')




@app.route('/Comunidad', methods =["GET", "POST"])
def subComunidad():
    
    if request.method == "POST":
        subcategory=request.form['subcomunidad']
        user_details.update({'subcategory':subcategory})
        comunidadsub=subcategory.replace(',','').replace(' ','').replace('text=','')
        if comunidadsub=='Músicosgruposmusicales':
            return redirect(url_for('Músicosgruposmusicales'))
        else:
            return redirect(url_for('finish'))
    return render_template('Comunidad.html')

@app.route('/Músicosgruposmusicales',methods=['GET','POST'])
def Músicosgruposmusicales():
    if request.method == "POST":
        subsubcategory=request.form['subsubcomunidad']
        user_details.update({'subsubcategory':subsubcategory})
        comunidadsub=subsubcategory.replace(',','').replace(' ','').replace('text=','')

        return redirect(url_for('finish'))
    return render_template('Músicosgruposmusicales.html')






@app.route('/Contactos', methods =["GET", "POST"])
def subContactos():

    if request.method == "POST":
        subcategory=request.form['subcontact']
        age=request.form['Age']
        user_details.update({'subcategory':subcategory,'Age':age})
        contactsub=subcategory.replace(',','').replace(' ','').replace('text=','').replace('etc...','').replace('(','').replace(')','')
        return redirect(url_for(f'{contactsub}'))
    return render_template('Contactos.html')


@app.route('/Relacionesocasionales', methods =["GET", "POST"])
def Relacionesocasionales():

    if request.method == "POST":
        subsubcategory=request.form['subsubcontact']
        user_details.update({'subsubcategory':subsubcategory})
        contactsub=subsubcategory.replace(',','').replace(' ','').replace('text=','').replace('etc...','').replace('(','').replace(')','')
        return redirect(url_for('finish'))
    return render_template('Relacionesocasionales.html')

@app.route('/Relacionesserias', methods =["GET", "POST"])
def Relacionesserias():

    if request.method == "POST":
        subsubcategory=request.form['subsubcontact']
        user_details.update({'subsubcategory':subsubcategory})
        contactsub=subsubcategory.replace(',','').replace(' ','').replace('text=','').replace('etc...','').replace('(','').replace(')','')
        return redirect(url_for('finish'))
    return render_template('Relacionesserias.html')

@app.route('/Servicioseróticosmasajes', methods =["GET", "POST"])
def Servicioseróticosmasajes():

    if request.method == "POST":
        subsubcategory=request.form['subsubcontact']
        user_details.update({'subsubcategory':subsubcategory})
        contactsub=subsubcategory.replace(',','').replace(' ','').replace('text=','').replace('etc...','').replace('(','').replace(')','')
        return redirect(url_for('finish'))
    return render_template('Servicioseróticosmasajes.html')















@app.route('/Eventos', methods =["GET", "POST"])
def subEventos():

    if request.method == "POST":
        subcategory=request.form['subeventos']
        startdate=request.form['startdate']
        enddate=request.form['enddate']
        user_details.update({'subcategory':subcategory,'start date':startdate,'end date':enddate})
        eventsub=subcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Eventos.html')








@app.route('/Inmobiliaria', methods =["GET", "POST"])
def subInmobiliaria():
  
    if request.method == "POST":
        subcategory=request.form['subinmobiliaria']
        price =request.form['Price']
        frequency=request.form['frequency']
        user_details.update({'subcategory':subcategory,'Price': price,'frequency':frequency})
        inmobiliariasub=subcategory.replace(',','').replace(' ','').replace('text=','').replace('/','')
        if inmobiliariasub=='Oficinaslocalesenalquiler':
            return redirect(url_for(f'{inmobiliariasub}'))
        elif inmobiliariasub=='Alquileresvacacionales':
            return redirect(url_for(f'{inmobiliariasub}'))
        elif inmobiliariasub=='Oficinaslocalesenventa':
            return redirect(url_for(f'{inmobiliariasub}'))
        else:
            return redirect(url_for('finish'))
    return render_template('Inmobiliaria.html')


@app.route('/Oficinaslocalesenalquiler', methods =["GET", "POST"])
def Oficinaslocalesenalquiler():

    if request.method == "POST":
        subsubcategory=request.form['subcontact']
        user_details.update({'subsubcategory':subsubcategory})
        contactsub=subsubcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Oficinaslocalesenalquiler.html')

@app.route('/Alquileresvacacionales', methods =["GET", "POST"])
def Alquileresvacacionales():

    if request.method == "POST":
        subsubcategory=request.form['subcontact']
        user_details.update({'subsubcategory':subsubcategory})
        contactsub=subsubcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Alquileresvacacionales.html')

@app.route('/Oficinaslocalesenventa', methods =["GET", "POST"])
def Oficinaslocalesenventa():

    if request.method == "POST":
        subsubcategory=request.form['subcontact']
        user_details.update({'subsubcategory':subsubcategory})
        contactsub=subsubcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Oficinaslocalesenventa.html')









@app.route('/Servicios', methods =["GET", "POST"])
def subServicios():
    if request.method == "POST":
        subcategory=request.form['subServicio']
        user_details.update({'subcategory':subcategory})
        servicesub=subcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Servicios.html')


@app.route('/Trabajo', methods =["GET", "POST"])
def subTrabajo():
  
    if request.method == "POST":
        subcategory=request.form['subTrabajo']
        user_details.update({'subcategory':subcategory})
        trabajosub=subcategory.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    return render_template('Trabajo.html')


@app.route('/Vehículos', methods =["GET", "POST"])
def subVehículos():
    
    if request.method == "POST":
        subVehiculo=request.form['subVehiculo']
        model=request.form['model']
        color=request.form['color']
        price=request.form['Price']
        state=request.form['state']
        year=request.form['year']
        transmission=request.form['transmission']
        kilometrage=request.form['kilometrage']
        Combustible=request.form['Combustible']
        body_type=request.form['body type']
        user_details.update({'subcategory':subVehiculo,
                             'modelo':model,
                             'color':color,
                             'Price':price,
                             'State':state,
                             'year':year,
                             'transmission':transmission,
                             'kilometrage':kilometrage,
                             'Combustible':Combustible,
                             'body type':body_type
                        })
        vehiculosub=subVehiculo.replace(',','').replace(' ','').replace('text=','')
        return redirect(url_for('finish'))
    
    return render_template('Vehículos.html')



@app.route('/finish', methods =["GET", "POST"])
def finish():
    try:
        collection.insert_one(user_details)
        
    except Exception as e  :
        pass
    return render_template('finish.html')


def automate():
    global user
    user=collection.find_one(user_details)
    
    email=user['email']
    password=user['password']
    title=user['title']
    
    
    city=user['city']
    category=user['category']
    subcategory=user['subcategory']
    description=user['description']

    try:
        state=user['State']
    except :
        pass

    try:
        transmission=user['transmission']
    except :
        pass

      
    try:       
        subsubcategory=user['subsubcategory']
    except:
        pass

        
          
    playwright=sync_playwright().start()  
    browser = playwright.chromium.launch(channel="chrome",headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://www.locanto.es/")
    page.locator("text=Iniciar sesión / Registrarse").click()
    page.locator("label").first.click()
    page.locator("text=mantener sesión activa Iniciar sesión Iniciar sesión sin contraseña o >> input[name=\"email\"]").fill(email)
    page.locator("label").nth(1).click()
    page.locator("input[name=\"pwd\"]").fill(password)
    page.locator("button:has-text(\"Iniciar sesión\")").first.click()
    page.wait_for_url("https://www.locanto.es/")
    page.wait_for_timeout(7000)
    page.wait_for_selector("span:has-text(\"Publicar un anuncio\")",).click()
    page.wait_for_url("https://www.locanto.es/post/")
    page.wait_for_selector("[placeholder=\"p\\.ej\\. Mercedes CLK 350 2008 en venta\"]").click()
    page.wait_for_timeout(10000)
    page.wait_for_selector("[placeholder=\"p\\.ej\\. Mercedes CLK 350 2008 en venta\"]").fill(title)
    page.wait_for_selector("[placeholder=\"p\\.ej\\. Mercedes CLK 350 2008 en venta\"]").press("Enter")
    page.locator("button:has-text(\"Continuar »\")").click()
    page.locator(f"{category}").click()
    page.locator(f"{subcategory}").click()
    try:
        page.locator(f"{subsubcategory}").click()
    except:
        pass
    page.locator("textarea[name=\"description\"]").click()
    page.locator("textarea[name=\"description\"]").fill(description)
    
    try:
        direction=user['direction']
        page.locator("input[name=\"mapStreet\"]").click()
        page.locator("input[name=\"mapStreet\"]").fill(direction)
    except :
        pass
    try:
        postal=user['code postal']
        page.locator("input[name=\"mapZip\"]").click()
        page.locator("input[name=\"mapZip\"]").fill(postal)
    except :
        pass
    
    page.locator("input[name=\"mapCity\"]").click()
    page.locator("input[name=\"mapCity\"]").fill(city)
    page.wait_for_timeout(2000)
    try:
        imagepath=user['image path']
        with page.expect_file_chooser() as fc_info:
            page.wait_for_selector("#js-img_box div").click()
            file_chooser = fc_info.value
            file_chooser.set_files(imagepath)
            page.wait_for_timeout(10000)
    except Exception as e :
        pass

    try:
        start_date=user['start date']
        page.locator("input[name=\"start_date\"]").click()
        page.locator("input[name=\"start_date\"]").fill(start_date)
        page.locator("input[name=\"start_date\"]").press('Enter')
    except:
        pass
    try:
        end_date=user['end date']
        page.locator("input[name=\"end_date\"]").click()
        page.locator("input[name=\"end_date\"]").fill(end_date)
        page.locator("input[name=\"end_date\"]").click()
        
    except:
        pass
    try:
        age=user['Age']
        page.locator("input[name=\"age\"]").click()
        page.locator("input[name=\"age\"]").fill(age)
    except :
        pass
    
    try:
        price=user['Price']
        page.locator("input[name=\"price\"]").click()
        page.locator("input[name=\"price\"]").fill(price)
    except :
        pass
    
    try:
        frequency=user['frequency']
        page.locator("select[name=\"itv\"]").select_option(frequency)
    except :
        pass
    try:
        model=user['modelo']
        page.locator("select[name=\"model\"]").select_option(model)
    except :
        pass
    try:
        page.locator(f"text={state}").click()
    except :
        pass
    try:
        year=user['year']
        page.locator("select[name=\"year\"]").select_option(year)
    except :
        pass
    try:
        color=user['color']
        page.locator("select[name=\"color\"]").select_option(color)
    except :
        pass
    try:
        page.locator(f"text={transmission}").click()
    except :
        pass
    try:
        kilometrage=user['kilometrage']
        page.locator("input[name=\"mileage\"]").click()
        page.locator("input[name=\"mileage\"]").fill(kilometrage)
    except :
        pass
    try:
        combustible=user['Combustible']
        page.locator("select[name=\"fuel\"]").select_option(combustible)
    except :
        pass
    try:
        body_type=user['body type']
        page.locator("select[name=\"body_style\"]").select_option(body_type)
    except :
        pass
    try:
        phone_number=user['phone number']
        page.locator("select[name=\"phone_number\"]").select_option("n")
        page.locator("input[name=\"phone_number_input\"]").click()
        page.locator("input[name=\"phone_number_input\"]").fill(phone_number)
    except :
        pass
    
    try:
        website=user['website']
        page.locator("[placeholder=\"http\\:\\/\\/\"]").click()
        page.locator("[placeholder=\"http\\:\\/\\/\"]").fill(website)
    except :
        pass
    try:

        page.locator("text=Publicar anuncio »").click()

        
        page.wait_for_timeout(10000)
        context.close()
        browser.close()
    except :
        pass
    
    
        
@app.route('/result',methods=["GET","POST"])      
def execute():
    user=collection.find_one(user_details)

    return render_template('success.html',userwork=user)      

@app.route('/execute',methods=["GET","POST"])  
def main():
    if request.method=="POST":
        return render_template("execution.html",automation=automate)
 
        
@app.route('/automate')
def summon():
    automate()

    today = datetime.date.today()
    second_date=user['redo date']
    second_date = datetime.datetime.strptime(second_date, '%Y-%m-%d').date()
    left=second_date-today
    
    if left==0:
        automate()
        redoday = today + datetime.timedelta(days=42)
        today=str(today)
        redoday=str(redoday)
        user.update({'date':today,'redo date':redoday})
        collection.delete_one({'_id':user['_id']})
        collection.insert_one(user)
    left=str(left)
    dayis=left[:2]
    return render_template('success.html',userwork=user, days=dayis)
        


if __name__=='__main__': 
    app.run(debug=True)


    
    











