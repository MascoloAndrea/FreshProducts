from doctest import Example
from importlib.resources import contents
from itertools import product
from msilib.schema import Error
from signal import valid_signals
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from App_FreshProducts.models import Licenze, Punto_vendita, Magazzino, Prodotto

#from FreshProducts.App_FreshProducts.models import Punto_vendita
#from FreshProducts.bc.models.licenze import licenze
#from FreshProducts.App_FreshProducts.models import Punto_vendita

'''
X RICERCA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
try:
    pers_type = Person_Type.objects.get(pers_type='Appelant')
except Person_Type.DoesNotExists:
    person_type = Person_Type.objects.create(pers_type='Appellant')
Person.objects.create(name='Adam', pers_type=pers_type)
'''
values = {}



# views sito vetrina -- INIZIO ---
def index(request):
    # view di base che mostra la homepage del sito vetrina
    templates = loader.get_template('Homepage.html')
    return HttpResponse(templates.render())

def registrer(request):
    # view che mostra la sezione di registrazione del sito vetrina
    templates = loader.get_template('Registrer.html')
    return HttpResponse(templates.render())

def contact(request):
    # view che mostra la sezione contatti del sito vetrina
    templates = loader.get_template('Contact.html')
    return HttpResponse(templates.render())

# views sito vetrina -- FINE ---


# views area riservata -- INIZIO --
def get_private_data(request):
    '''Funzione che recupera tutti i dati dell'utenza'''
    global values
    values = Punto_vendita.objects.filter(user=request.user.id).values()[0]
    totale_prodotti = Magazzino.objects.filter(Shop_code=values['Shop_code']).count()
    today = datetime.now().strftime('%Y-%m-%d')
    start_date = datetime.strptime("2000-01-01", '%Y-%m-%d')
    next_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    in_scadenza = Magazzino.objects.filter(Shop_code=values['Shop_code'],Scadenza__range=(start_date, next_week)).count()
    scaduti = Magazzino.objects.filter(Shop_code=values['Shop_code'],Scadenza__range=(start_date, yesterday)).count()
    
    #try:
        #no_scadenza = Magazzino.objects.filter(Scadenza=None).count()
    #except: obj
        #print("Errore")
        #no_scadenza = 0
    no_scadenza = Magazzino.objects.filter(Shop_code=values['Shop_code'],Scadenza__isnull=True).count()
    #print()
    #print(no_scadenza)
    #print(values)
    licenze = Licenze.objects.filter(Code=values['Code_id']).values()[0]
    # tab.objects.raw("SELECT...")
    values = values | licenze # merge of two dict
    user = User.objects.filter(username=request.user.username).values()[0]
    user['date_joined'] = (user['date_joined'] + timedelta(hours=2))
    user['last_login'] = (user['last_login'] + timedelta(hours=2)) # orario server 2 ore indietro
    values = values | user # merge of two dict
    #print(user)
    #print("ID: ",request.user.id)
    #print(values)
    #print()
    values['today'] = today
    values['next_week'] = next_week
    values['yesterday'] = yesterday
    values['start_date'] = start_date
    values['totale_prodotti'] = totale_prodotti
    values['in_scadenza'] = in_scadenza
    values['scaduti'] = scaduti
    values['no_scadenza'] = no_scadenza
    return values

def area_riservata(request):
    global values
    values['state'] = 0
    # view che mostra l'area riservata dell'utente
    if request.user.is_authenticated:
        # se l'utente è autenticato mostra la pagina
        
        #print(request.user)
        #print(request)
        #print(User.first_name[0])
        #print(User.objects.get(username=request.user.username))
        #print(Punto_vendita.objects.get(Username=request.user.username))
        #Punto_vendita.objects.filter(Username=request.user.username)
        #ris = Punto_vendita.objects.filter(user=request.user.id)
        #ris = Punto_vendita.objects.all()[0] #prende il primo
        '''
        per ottenere oggetto:

        ris = Punto_vendita.objects.get(user=request.user.id)

        per ottenere queryset:

        ris = Punto_vendita.objects.filter(user=request.user.id).values()[0]
        ris -> dizionario -> {'Shop_code':1,...}
        '''
        values = get_private_data(request)
        #ris = 1
        
        #ris.values('Nome').get()
        
        templates = loader.get_template('Area_riservata.html')
        return HttpResponse(templates.render(values, request))
        #return HttpResponse(templates.render()) # return senza values
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')


# views new products -- INIZIO --
def new_product(request):
    # view che mostra l'area riservata dell'utente
    if request.user.is_authenticated:
        # se l'utente è autenticato mostra la pagina
        
        #print(request.user)
        #print(request)
        #print(User.first_name[0])
        #print(User.objects.get(username=request.user.username))
        #print(Punto_vendita.objects.get(Username=request.user.username))
        #Punto_vendita.objects.filter(Username=request.user.username)
        #ris = Punto_vendita.objects.filter(user=request.user.id)
        #ris = Punto_vendita.objects.all()[0] #prende il primo
        
        values = get_private_data(request)
        #ris = 1
        values['state'] = 0
        values['submit_message'] = "Verifica Barcode"
        #ris.values('Nome').get()
        
        templates = loader.get_template('New_products.html')
        return HttpResponse(templates.render(values, request))
        #return HttpResponse(templates.render()) # return senza values
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

def process(request):
    #print("process function is called")
    if request.method == "POST":
        barcode = request.POST['barcode']
        results = Prodotto.objects.filter(Barcode=barcode)
        if results.exists():
            # se ci sono risultati -> prodotto gia presente
            #print("codice esiste")
            results = results.values()[0]
            values['Nome_prodotto'] = results["Nome"]
            values['Marca_prodotto'] = results["Marca"]
            values['Barcode'] = results["Barcode"]
            values['state'] = 1
        else:
            # non ci sono risultati -> prodotto nuovo
            values['state'] = 2
            values['Barcode'] = barcode
            #print("codice non esiste")
        values['submit_message'] = "Salva"#"Aggiungi prodotto"
        #print(barcode)
        templates = loader.get_template('New_products.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

def executed(request):
    '''Funzione che esegue l'aggiunta dei prodotti nel magazzino
    restituisce:
        - pagina del form nel caso di errore
        - pagina di completamento nel caso di caricamento effettuato'''
    global values
    if request.method == "POST":
        #print(request.POST)
        # controllo dello state per capire se il prodotto è gia in lista
        if values['state'] == 1:
            #prodotto gia presente
            try:
                #print("Prodotto gia presente")
                #print(request.POST['Scadenza'])
                prodotto = Prodotto.objects.get(Barcode=values['Barcode'])
                shop = Punto_vendita.objects.get(Shop_code=values['Shop_code'])
                Quantita = request.POST['Quantita']
                Prezzo = request.POST['Prezzo']
                Reparto = request.POST['Reparto'].title()
                #print(request.POST)
                Scadenza = request.POST['Scadenza']
                if Scadenza == "":
                    Scadenza = None
                magazzino = Magazzino.objects.create(
                    Barcode = prodotto, 
                    Shop_code = shop,
                    Quantita = Quantita,
                    Reparto = Reparto,
                    Prezzo = Prezzo,
                    Scadenza = Scadenza
                )
                values['state'] = 3 # prodotto aggiunto con successo
                values['esito'] = "Prodotto aggiunto con successo!"
            except IntegrityError as e:
                values['state'] = 4 # errore
                #print(e)
                values['esito'] = "Impossibile completare l'operazione. Il prodotto è gia presente nella banca dati. Se si intende modificarlo andare nella sezione modifica prodotto."
            except:
                values['state'] = 4 # errore
                values['esito'] = "Si è verificato un problema nell'inserimento del prodotto. Si prega di contattare il servizio clienti per assistenza."

        elif values['state'] == 2:
            #prodotto nuovo da aggiungere
            try:
                Barcode = values['Barcode']
                Nome = request.POST['Nome'].title()
                Marca = request.POST['Marca'].title()
                prodotto = Prodotto.objects.create(Barcode=Barcode, Nome=Nome, Marca=Marca)
                shop = Punto_vendita.objects.get(Shop_code=values['Shop_code'])
                Quantita = request.POST['Quantita']
                Prezzo = request.POST['Prezzo']
                Reparto = request.POST['Reparto'].title()
                #print(request.POST)
                Scadenza = request.POST['Scadenza']
                if Scadenza == "":
                    Scadenza = None
                magazzino = Magazzino.objects.create(
                    Barcode = prodotto, 
                    Shop_code = shop,
                    Quantita = Quantita,
                    Reparto = Reparto,
                    Prezzo = Prezzo,
                    Scadenza = Scadenza
                )
                #print("Scadenza: ", Scadenza)
                #print("Nuovo prodotto")
                values['state'] = 3 # prodotto aggiunto con successo
                values['esito'] = "Prodotto aggiunto con successo!"
            except:
                values['state'] = 4 # errore
                values['esito'] = "Si è verificato un problema nell'inserimento del prodotto. Si prega di contattare il servizio clienti per assistenza."
        else:
            #errore codice state errato
            values['state'] = 4 # errore
            values['esito'] = "Si è verificato un problema nella gestione degli state. Si prega di contattare il servizio clienti per assistenza."
        templates = loader.get_template('New_products.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')
# views new products -- FINE --




def remove_products(request):
    global values
    if request.user.is_authenticated:
        values['state'] = 0
        if request.method == "POST":
            barcode = request.POST['barcode']
            prodotto = list(Magazzino.objects.filter(Shop_code=values['Shop_code'], Barcode=barcode).values())
            if len(prodotto) == 1:
                # procedere con eliminazione prodotto
                instance = Magazzino.objects.get(Shop_code=values['Shop_code'], Barcode=barcode)
                instance.delete()
                values['state'] = 3
                values['esito'] = "Prodotto rimosso con successo!"
            elif len(prodotto) < 1:
                # Errore barcode inesistente
                values['state'] = 4
                values['esito'] = "Il codice prodotto inserito non è corretto o è inesistente."
            else:
                # errore generico
                values['state'] = 4
                values['esito'] = "Si è verificato un errore imprevisto nella rimozione del prodotto. Contattare il servizio clienti per l'assistenza."
            #print(prodotto)
        templates = loader.get_template('Remove_products.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')






# views area riservata -- FINE --









def AccessDenied(request):
    # view per l'accesso negato in quanto non è stato effettuato il login
    templates = loader.get_template('Error_403.html')
    return HttpResponse(templates.render())




def signin(request):
    # view che mostra il form di autenticazione
    if request.user.is_authenticated:
        # se user già autenticato redirect all'area personale
        return HttpResponseRedirect('/area_riservata')
    # se l'utente non è registrato
    # mostra la pagina per effettuare l'accesso all'area riservata
    # può esserci un errore dovuto a un tentativo di accesso passato
    txt = {}
    if request.method == "POST":
        # se il metodo della richiesta è post
        username = request.POST['username']
        password = request.POST['password']
        #print("Entrato nel POST")
        # passaggio dei parametri per effettuare il login

        user = authenticate(username=username, password=password) 
        # autenticazione dell'utente
        if user is not None:
            # utente correttamente autenticato -> username e password hanno una corrispondenza
            # controllo licenza non scaduta
            
            user_instance = User.objects.filter(username=username).values()[0]
            # prendo l'istanza dell'utente appena loggato
            #print(user_instance)
            # ricerco il punto vendita per questo utente
            shop_instance = Punto_vendita.objects.filter(user=user_instance['id']).values()[0]
            #print(shop_instance)
            # risalgo alla licenza d'uso per questo punto vendita
            licenza_instance = Licenze.objects.filter(Code=shop_instance['Code_id']).values()[0]
            #print(licenza_instance)
            # controllo data scadenza
            data_scadenza = licenza_instance['Data_scadenza'] # datetime format
            #print(data_scadenza, type(data_scadenza))
            today = datetime.now().date() # datetime format of today
            if data_scadenza >= today:
                # licenza non scaduta
                login(request, user)
                #print("utente autenticato")
                #print(request.user, ": ", request.user.id)
                # login dell'utente con passaggio della richiesta e l'autenticazione
                #name = user.elem
                return HttpResponseRedirect('/area_riservata')
                # redirect all'area riservata dell'utente
            else:
                # licenza scaduta
                txt['error'] = "⚠ La licenza d'uso associata a questo account è scaduta. Contattare il servizio clienti per il rinnovo."
        else:
            #print("utente non autenticato")
            # utente non autenticato correttamente
            # mostra messaggio di errore
            #return render(request, "./templates/login.html", {'error': error})
            #messages.error(request, "Credenziali errate")
            txt['error'] = "⚠ Credenziali errate: username o password non validi!"
            #messages.error(request, "⚠ Credenziali errate: username o password non validi!")
            #return HttpResponseRedirect('/home/login/?error='+ error_context)


    

    templates = loader.get_template('Login.html')
    return HttpResponse(templates.render(txt, request))


def signout(request):
    global values
    values['state'] = 0
    # view per il logout degli utenti
    logout(request) # logout utente
    # redirect alla schermata home del sito vetrina
    return HttpResponseRedirect('/home/') 

def getProductsForTable(request, products):
    '''Funzione che crea e restituisce una lista di dizionari con tutti i dati dei
    prodotti contenuti nel magazzino del negozio. Restituisce il dizionario globale
    con l'aggiunta del parametro values['table']
    
    In parametro la request e i prodotti e una lista di dizionari dei prodotti
    a cui aggiunge: nome e marca dei prodotti e mette in ordine di tabella tutti gli 
    attributi.
    '''
    values = get_private_data(request) # richiesta dati normali
    # richiesta di tutti i prodotti legati al punto vendita (Shop_code)
    
    #print(all_products)
    
    for diz in products:
        # per ogni prodotto (in forma di diz) nella lista trova nome e marca
        product = Prodotto.objects.filter(Barcode=diz['Barcode_id']).values('Nome', 'Marca')[0]
        #print(diz)
        # salvataggio di nome e marca al dizionario del prodotto in questione
        diz['Nome'] = product['Nome']
        diz['Marca'] = product['Marca']
        # sostituzione stringa vuota se scadenza = None
        if diz['Scadenza'] == None:
            diz['Scadenza'] = ""
        #print(diz)
    #print(all_products)
    newDiz = {}
    lista = []
    # for per sistemazione in ordine del dizionario
    for diz in products:
        newDiz = {}
        newDiz['Barcode_id'] = diz['Barcode_id']
        newDiz['Nome'] = diz['Nome']
        newDiz['Marca'] = diz['Marca']
        newDiz['Quantita'] = diz['Quantita']
        newDiz['Reparto'] = diz['Reparto']
        newDiz['Prezzo'] = diz['Prezzo']
        newDiz['Scadenza'] = diz['Scadenza']
        lista.append(newDiz)
    values['table'] = lista # aggiunta lista di dizionari al dizionario globale alla voce table
    values['table_len'] = len(lista)
    return values


def catalogo(request):
    global values
    
    if request.user.is_authenticated:
        values = get_private_data(request)
        all_products = list(Magazzino.objects.filter(Shop_code=values['Shop_code']).values('Barcode_id', 'Quantita', 'Reparto', 'Prezzo', 'Scadenza'))
        values = getProductsForTable(request, all_products)
        templates = loader.get_template('Catalogo.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

def expiry_date(request):
    global values
    if request.user.is_authenticated:
        all_products = list(Magazzino.objects.filter(Shop_code=values['Shop_code'], Scadenza__isnull=False).values('Barcode_id', 'Quantita', 'Reparto', 'Prezzo', 'Scadenza'))
        values = getProductsForTable(request, all_products)
        if request.method == "POST":
            order = request.POST['criteri']
            #print("Entrato nel POST")
            #print(order, type(order))
            if order == "1":
                # ordine di scadenza
                parametro = 'Scadenza'
                     
                #print(1)
            elif order == "2":
                # ordine decrescente
                parametro = '-Scadenza'
                #print(2)
            else:
                # errore
                pass
            all_products = list(Magazzino.objects.filter(Shop_code=values['Shop_code'], Scadenza__isnull=False).values('Barcode_id', 'Quantita', 'Reparto', 'Prezzo', 'Scadenza').order_by(parametro))
            values = getProductsForTable(request, all_products)
            
        templates = loader.get_template('Expiry_date.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

def area_utente(request):
    global values
    if request.user.is_authenticated:
        if request.method == "POST":
            punto_vendita = request.POST['punto_vendita']
            indirizzo = request.POST['indirizzo']
            civico = request.POST['civico']
            citta = request.POST['citta']
            cap = request.POST['cap']
            if punto_vendita != "": 
                Punto_vendita.objects.filter(Shop_code=values['Shop_code']).update(Nome=punto_vendita)
            if indirizzo != "":
                Punto_vendita.objects.filter(Shop_code=values['Shop_code']).update(Indirizzo=indirizzo)
            if civico != "":
                Punto_vendita.objects.filter(Shop_code=values['Shop_code']).update(Civico=civico)
            if citta != "":
                Punto_vendita.objects.filter(Shop_code=values['Shop_code']).update(Citta=citta)
            if cap != "":
                Punto_vendita.objects.filter(Shop_code=values['Shop_code']).update(Cap=cap)
            values = get_private_data(request)
        templates = loader.get_template('Area_utente.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')


def modify_product(request):
    global values
    if request.user.is_authenticated:
        values['submit_message'] = "Verifica Barcode"
        values['state'] = 0
        if request.method == "POST":
            barcode = request.POST['barcode']
            prod_magazzino = list(Magazzino.objects.filter(Shop_code=values['Shop_code'], Barcode=barcode).values())
            if len(prod_magazzino) == 1:
                # procedere con modifica prodotto
                prod_magazzino = prod_magazzino[0]
                prodotto = Prodotto.objects.filter(Barcode=barcode).values()[0]
                values['Nome_prodotto'] = prodotto["Nome"]
                values['Marca_prodotto'] = prodotto["Marca"]
                values['Barcode'] = prodotto["Barcode"]
                values['Quantita'] = prod_magazzino["Quantita"]
                values['Reparto'] = prod_magazzino["Reparto"]
                values['Prezzo'] = prod_magazzino["Prezzo"]
                values['Scadenza'] = prod_magazzino["Scadenza"]
                values['submit_message'] = "Modifica Prodotto"
                values['state'] = 1
            elif len(prod_magazzino) < 1:
                # Errore barcode inesistente
                values['state'] = 4
                values['esito'] = "Il codice prodotto inserito non è corretto o è inesistente."
            else:
                # errore generico
                values['state'] = 4
                values['esito'] = "Si è verificato un errore imprevisto nella modifica del prodotto. Contattare il servizio clienti per l'assistenza."
            #print(prod_magazzino)
        templates = loader.get_template('Modify_product.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

def process_modify_prod(request):
    global values
    if request.user.is_authenticated:
        if request.method == "POST":
            Quantita = request.POST['Quantita']
            Prezzo = request.POST['Prezzo']
            Reparto = request.POST['Reparto'].title()
            Scadenza = request.POST['Scadenza']
            if Quantita != "": 
                Magazzino.objects.filter(Shop_code=values['Shop_code'], Barcode=values['Barcode']).update(Quantita=Quantita)
            if Prezzo != "":
                Magazzino.objects.filter(Shop_code=values['Shop_code'], Barcode=values['Barcode']).update(Prezzo=Prezzo)
            if Reparto != "":
                Magazzino.objects.filter(Shop_code=values['Shop_code'], Barcode=values['Barcode']).update(Reparto=Reparto)
            if Scadenza != "":
                Magazzino.objects.filter(Shop_code=values['Shop_code'], Barcode=values['Barcode']).update(Scadenza=Scadenza)
            values['state'] = 3
            values['esito'] = "Il prodotto è stato modificato correttamente"
        templates = loader.get_template('Modify_product.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

def product(request):
    global values
    
    if request.user.is_authenticated:
        values = get_private_data(request)
        templates = loader.get_template('Product.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

def prox_to_scadenza(request):
    global values
    
    if request.user.is_authenticated:
        values = get_private_data(request)
        in_scadenza = list(Magazzino.objects.filter(Shop_code=values['Shop_code'],Scadenza__range=(values['today'], values['next_week'])).values('Barcode_id', 'Quantita', 'Reparto', 'Prezzo', 'Scadenza').order_by('Scadenza'))
        values = getProductsForTable(request, in_scadenza)
        
        templates = loader.get_template('Catalogo.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

def without_scadenza(request):
    global values
    
    if request.user.is_authenticated:
        values = get_private_data(request)
        no_scadenza = Magazzino.objects.filter(Shop_code=values['Shop_code'],Scadenza__isnull=True).values()
        values = getProductsForTable(request, no_scadenza)

        templates = loader.get_template('Catalogo.html')
        return HttpResponse(templates.render(values, request))
        
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

def article_scad(request):
    global values
    
    if request.user.is_authenticated:
        values = get_private_data(request)
        scaduti = list(Magazzino.objects.filter(Shop_code=values['Shop_code'],Scadenza__range=(values['start_date'],values['yesterday'])).values())
        #print(scaduti)
        #print(values['start_date'],values['yesterday'])
        values = getProductsForTable(request, scaduti)

        templates = loader.get_template('Catalogo.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

def assistance(request):
    global values
    
    if request.user.is_authenticated:
        values = get_private_data(request)
        templates = loader.get_template('Assistance.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

def settings(request):
    global values
    
    if request.user.is_authenticated:
        values = get_private_data(request)
        if request.method == "POST":
            #print(request.POST)
            old_psw = request.POST['old_psw']
            new_psw1 = request.POST['new_psw1']
            new_psw2 = request.POST['new_psw2']
            if request.user.check_password(old_psw):
                # password vecchia corretta
                #print("password corretta")
                if new_psw1 == new_psw2:
                    # controllo corrispondenza nuove psw
                    request.user.set_password(new_psw1)
                    request.user.save()
                    # cambio password
                    values['esito'] = 1
                    values['msg'] = "Password modificata con successo!"
                    templates = loader.get_template('Password_changed.html')
                    return HttpResponse(templates.render(values, request))
                else:
                    # password non corrispondono
                    values['esito'] = 0
                    values['msg'] = "Errore ⚠: Le password non corrispondono"
            else:
                # password vecchia sbagliata
                values['esito'] = 0
                values['msg'] = "⚠ Password non valida"
        templates = loader.get_template('Settings.html')
        return HttpResponse(templates.render(values, request))
    else:
        # se non è autenticato mostra il file Error_403.html di errore
        return HttpResponseRedirect('/error403')

'''
def process(request):
    # view che processa il login da parte degli utenti
    #if request.user.is_authenticated:
    if request.method == "POST":
        # se il metodo della richiesta è post
        username = request.POST['username']
        password = request.POST['password']
        # passaggio dei parametri per effettuare il login

        user = authenticate(username=username, password=password) 
        # autenticazione dell'utente
        if user is not None:
            # utente correttamente autenticato
            login(request, user)
            # login dell'utente con passaggio della richiesta e l'autenticazione
            #name = user.elem
            return HttpResponseRedirect('/area_riservata')
            # redirect all'area riservata dell'utente
        else:
            # utente non autenticato correttamente
            # mostra messaggio di errore
            #return render(request, "./templates/login.html", {'error': error})
            #messages.error(request, "Credenziali errate")
            return HttpResponseRedirect('/home/login/?wrong=true')
            #return HttpResponseRedirect('/home/login/?error='+ error_context)
    else:
        # se il metodo è diverso da post mostra la pagina di login
        return HttpResponseRedirect('/home/login')
'''




'''
Funzioni di login
#################################################################
def signin(request):
    # view che mostra il form di autenticazione
    if request.user.is_authenticated:
        # se user già autenticato redirect all'area personale
        return HttpResponseRedirect('/area_riservata')
    # se l'utente non è registrato
    # mostra la pagina per effettuare l'accesso all'area riservata
    # può esserci un errore dovuto a un tentativo di accesso passato
    
    #context = {}

    #try:
        #errore = request.GET["error"]
        #context["error"] = errore
        #print(errore)
    #except Exception as e:
        #print("Dettagli errore: ",e)
    
    error_msg = {}
    try:
        errore = request.GET["wrong"] # se fa il get è presente errore
        if errore == "true":
            error_msg['error'] = "⚠ Credenziali errate: username o password non validi!"
    except Exception as e:
        print("Dettagli errore: ",e)
    

    templates = loader.get_template('Login.html')
    return HttpResponse(templates.render(error_msg, request))

def process(request):
    # view che processa il login da parte degli utenti
    #if request.user.is_authenticated:
    if request.method == "POST":
        # se il metodo della richiesta è post
        username = request.POST['username']
        password = request.POST['password']
        # passaggio dei parametri per effettuare il login

        user = authenticate(username=username, password=password) 
        # autenticazione dell'utente
        if user is not None:
            # utente correttamente autenticato
            login(request, user)
            # login dell'utente con passaggio della richiesta e l'autenticazione
            #name = user.elem
            return HttpResponseRedirect('/area_riservata')
            # redirect all'area riservata dell'utente
        else:
            # utente non autenticato correttamente
            # mostra messaggio di errore
            #return render(request, "./templates/login.html", {'error': error})
            #messages.error(request, "Credenziali errate")
            return HttpResponseRedirect('/home/login/?wrong=true')
            #return HttpResponseRedirect('/home/login/?error='+ error_context)
    else:
        # se il metodo è diverso da post mostra la pagina di login
        return HttpResponseRedirect('/home/login')











Funzione di registrazione
#################################################################


def signup(request):
    #funzione di registrazione collegata al form di registrazione
    if request.method == "POST":
        #username = request.POST.get('username')
        username = request.POST['username'] # tra virgolette il name del tag input html
        email = request.POST['email']
        password = request.POST['password']
        elem = request.POST['elem']

        myuser = User.objects.create_user(username, email, password) # accede all'utente
        myuser.elem = elem # associa i diversi attributi

        myuser.save() # effettua il salvataggio

        messages.success(request, "Il tuo account è stato correttamente creato." )

        return redirect('/home/login')

    pass
'''