import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Funció per obtenir els permisos de l'usuari actual des de la base de dades
def obtenir_permisos(username):
    conn = sqlite3.connect('xiringuito.db')
    cursor = conn.cursor()

    cursor.execute('SELECT Permisos FROM Users WHERE NomUsuari = ?', (username,))
    resultat = cursor.fetchone()

    if resultat:
        permisos_usuari = resultat[0]
    else:
        permisos_usuari = None

    conn.close()
    return permisos_usuari




# FINESTRA DE LOGIN I VALIDACIÓ DE CREDENCIALS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def mostrar_finestra_login():
    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry("300x150")
    
    tk.Label(login_window, text="Nom d'usuari:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()
    
    tk.Label(login_window, text="Contrasenya:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()
    
    def validar_login():
        username = username_entry.get()
        password = password_entry.get()
        
        # Validar les credencials amb la base de dades
        if validar_credencials(username, password):
            # Accés permès; tanca la finestra de login i mostra la finestra principal
            login_window.destroy()
            mostrar_finestra_principal(username)  # Passa el nom d'usuari a la finestra principal
        else:
            messagebox.showerror("Error", "Credencials incorrectes")

    tk.Button(login_window, text="Login", command=validar_login).pack()

    login_window.mainloop()

def validar_credencials(username, password):
    try:
        conn = sqlite3.connect('xiringuito.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM Users WHERE NomUsuari = ? AND Contrasenya = ?', (username, password))
        result = cursor.fetchone()
        
        if result:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("Error de la base de dades:", e)
    finally:
        if conn:
            conn.close()







#                                                   PRINCIPAL
            


# Creació de la finestra principal
root = tk.Tk()
root.title("XIRINGUITO XUPITET I BECAETA")
root.configure(bg="SteelBlue")
root.geometry("342x294")                    # Defineix el tamany de la finestra
root.resizable(width=False, height=False)   # Impedeix el redimensionament
button_font = ("Arial", 9, "bold")



def mostrar_finestra_principal(username):
    root.title("XIRINGUITO XUPITET I BECAETA")
    root.configure(bg="SteelBlue")
    root.geometry("342x294")                    # Defineix el tamany de la finestra
    root.resizable(width=False, height=False)   # Impedeix el redimensionament
    button_font = ("Arial", 9, "bold")

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Funció per a gestionar un nou lloguer
    def nou_lloguer():  
        nova_finestra = tk.Toplevel(root)
        nova_finestra.title("Nou Lloguer")
        nova_finestra.configure(bg="SteelBlue")

        # Calcula les coordenades per centrar la nova finestra respecte a la finestra principal
        x = root.winfo_x() + root.winfo_width() +2
        y = root.winfo_y()
        
        # Defineix les dimensions i la posició de la nova finestra
        nova_finestra.geometry(f"400x294+{x}+{y}")
        
        # Etiquetes i camps d'entrada per a codi de tumbona, DNI, nom i telèfon
        tk.Label(nova_finestra, text="Codi Tumbona:", bg="Gold").grid(row=0, column=0, padx=10, pady=5)
        codi_entry = tk.Entry(nova_finestra)
        codi_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(nova_finestra, text="DNI Usuari:", bg="Gold").grid(row=1, column=0, padx=10, pady=5)
        dni_entry = tk.Entry(nova_finestra)
        dni_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(nova_finestra, text="Nom Usuari:", bg="Gold").grid(row=2, column=0, padx=10, pady=5)
        nom_entry = tk.Entry(nova_finestra)
        nom_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(nova_finestra, text="Telèfon Usuari:", bg="Gold").grid(row=3, column=0, padx=10, pady=5)
        telefon_entry = tk.Entry(nova_finestra)
        telefon_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Funció per a gestionar el lloguer de la tumbona
        def llogar_tumbona():
            codi = codi_entry.get()
            dni = dni_entry.get()
            nom = nom_entry.get()
            telefon = telefon_entry.get()
            # Comprovació per a que el dni no siga null al llogar una tumbona
            if not dni:
                messagebox.showwarning("Advertència", "Si us plau, introdueix el DNI per poder llogar la tumbona.")
                return  # Eixir de la funció si el DNI està buit
            
            try:
                # Connexió a la base de dades
                conn = sqlite3.connect('xiringuito.db')
                cursor = conn.cursor()
                cursor.execute('SELECT estat FROM Tumbones WHERE codi = ?', (codi,))
                estatTumbona = cursor.fetchone()
                if estatTumbona and estatTumbona[0] == "Lliure":
                    # Inserció del nou lloguer amb clàusula INSERT OR IGNORE
                    cursor.execute('INSERT OR IGNORE INTO Usuaris (dni, nom, telefon) VALUES (?, ?, ?)', (dni, nom, telefon,))
                    
                    # Actualització de l'estat de la tumbona a "ocupada" i afegir data de lloguer
                    
                    cursor.execute('UPDATE Tumbones SET estat = "Ocupada" WHERE codi = ?', (codi,))
                    
                    # Actualització de la taula Lloguers
                    data_actual = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    cursor.execute('INSERT INTO Lloguers (Usuari, Tumbona, Data_Inici) VALUES (?, ?, ?)' , (dni, codi , data_actual,))
                    
                    # Guardem els canvis
                    conn.commit()
                
                    # Comprovar si s'ha realitzat el lloguer
                    if cursor.rowcount > 0:
                        messagebox.showinfo("Info", "Lloguer realitzat amb èxit")
                    else:
                        messagebox.showwarning("Advertència", "Aquest client ja té una tumbona llogada.")
                else:
                    messagebox.showwarning("Advertència", "Aquesta tumbona ja està ocupada.")
        
            except sqlite3.Error as e:
                messagebox.showerror("Error", str(e))
        
            finally:
                # Tanquem la connexió
                conn.close()
                nova_finestra.destroy()
    
        # Botó (pantalla emergent) per a llogar la tumbona
        llogar_button = tk.Button(nova_finestra, text="Llogar", width=53, height=5 , bg="Gold" , font=button_font, command=llogar_tumbona)
        llogar_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def cobrar_lloguer():
        permisos_Usuari=obtenir_permisos(username)
        if permisos_Usuari == 'Administrador':
            nova_finestra = tk.Toplevel(root)
            nova_finestra.title("Cobrar Lloguer")
            nova_finestra.configure(bg="SteelBlue")

            # Calcula les coordenades per centrar la nova finestra respecte a la finestra principal
            x = root.winfo_x() - root.winfo_width() -60
            y = root.winfo_y()
            
            # Defineix les dimensions i la posició de la nova finestra
            nova_finestra.geometry(f"400x164+{x}+{y}")
            
            tk.Label(nova_finestra, text="Codi Tumbona:", bg="Gold").grid(row=0, column=0, padx=10, pady=5)
            codi_entry = tk.Entry(nova_finestra)
            codi_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(nova_finestra, text="DNI Client:", bg="Gold").grid(row=1, column=0, padx=10, pady=5)
            dni_entry = tk.Entry(nova_finestra)
            dni_entry.grid(row=1, column=1, padx=10, pady=5)
            
            def calcular_cobrament():
                codi = codi_entry.get()
                dni = dni_entry.get()
                
                if codi and dni:  # Comprova que s'han introduït tant el codi de la tumbona com el DNI
                    try:
                        # Connexió a la base de dades
                        conn = sqlite3.connect('xiringuito.db')
                        cursor = conn.cursor()
                        
                        # Comprovar si el codi de la tumbona i el DNI de l'usuari coincideixen amb una entrada a la taula de lloguers
                        cursor.execute('SELECT COUNT(*) FROM Lloguers WHERE Tumbona = ? AND Usuari = ?', (codi, dni,))
                        existeix_lloguer = cursor.fetchone()[0]
                        
                        if existeix_lloguer > 0:  # Si s'ha trobat una coincidència
                            # Obtenir el preu del lloguer de la tumbona
                            cursor.execute('SELECT preu FROM Tumbones WHERE codi = ?', (codi,))
                            preu = cursor.fetchone()
                            
                            if preu:
                                preu = preu[0]
                                # Afegir el preu al recompte de beneficis
                                messagebox.showinfo("Info", f"Import cobrat: {preu} euros")
                                
                                # Actualitzar l'estat de la tumbona a "Lliure" i la data_Fi
                                cursor.execute('UPDATE Tumbones SET estat = "Lliure" WHERE codi = ?', (codi,))
                                data_actual = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                                cursor.execute('UPDATE Lloguers SET Data_Fi = ? WHERE Tumbona = ? AND Data_Fi IS NULL', (data_actual, codi,))
                                
                                # Guardar els canvis
                                conn.commit()
                            
                            else:
                                messagebox.showerror("Error", "No s'ha trobat cap tumbona amb aquest codi")
                        
                        else:
                            messagebox.showerror("Error", "El codi de la tumbona o el DNI de l'usuari no coincideixen amb cap entrada a la taula de lloguers")
                    
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", str(e))
                    
                    finally:
                        conn.close()
                        nova_finestra.destroy()
                
                else:
                    messagebox.showwarning("Advertència", "Si us plau, introdueix el codi de la tumbona i el DNI del client correctament.")

            # Botó (pantalla emergent) per a cobrar la tumbona
            cobrar_button = tk.Button(nova_finestra, text="Cobrar", width=53, height=5 , bg="Gold" , font=button_font, command=calcular_cobrament)
            cobrar_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        else:
            messagebox.showerror("Accés Denegat", "No tens permisos d'administrador per accedir a aquesta funcionalitat.")


    def mostrar_informacio_beneficis(benefici, tumbones_cobrades):
        # Crear una nova finestra
        nova_finestra = tk.Toplevel()
        nova_finestra.title("Recompte de Beneficis")
        nova_finestra.configure(bg="SteelBlue")
        x = root.winfo_x() - root.winfo_width() -60
        y = root.winfo_y() +196
        nova_finestra.geometry(f"400x164+{x}+{y}")
        
        if tumbones_cobrades is not None:
            # Crear etiqueta per mostrar el total de beneficis
            label_beneficis = tk.Label(nova_finestra, text=f"El total de beneficis és: {benefici} euros", bg="Gold", font=("Helvetica", 14))
            label_beneficis.pack(pady=20)
        else:
            # Crear etiqueta en cas de no haver-hi beneficis
            label_no_beneficis = tk.Label(nova_finestra, text="No hi ha cap tumbona llogada actualment.", bg="Gold", font=(button_font, 16))
            label_no_beneficis.pack(pady=20)
        
        # Mostrar la finestra
        nova_finestra.mainloop()

    def consultar_beneficis():
        permisos_Usuari=obtenir_permisos(username)
        if permisos_Usuari == 'Administrador':
            try:
                # Connexió a la base de dades
                conn = sqlite3.connect('xiringuito.db')
                cursor = conn.cursor()
                
                # Consulta per obtenir el recompte de beneficis
                cursor.execute('SELECT COUNT(*) FROM Lloguers WHERE Data_Fi IS NOT NULL')
                tumbones_cobrades = cursor.fetchone()
                cursor.execute('SELECT preu FROM Tumbones')
                preu_tumbona = cursor.fetchone()
                benefici = tumbones_cobrades[0] * preu_tumbona[0]
                # Tancar el cursor
                cursor.close()

                # Mostrar la informació de beneficis en una finestra personalitzada
                mostrar_informacio_beneficis(benefici, tumbones_cobrades)
                
            except sqlite3.Error as e:
                print("Error:", e)
                
            finally:
                # Tanquem la connexió
                conn.close()
        else:
            messagebox.showerror("Accés Denegat", "No tens permisos d'administrador per accedir a aquesta funcionalitat.")



    def mostrar_informacio(total_lliures, codis):
        # Crear una nova finestra
        nova_finestra = tk.Toplevel()
        nova_finestra.title("Informació de Tumbones Lliures")
        nova_finestra.configure(bg="SteelBlue")
        
        # Calcula les coordenades per centrar la nova finestra respecte a la finestra principal
        x = root.winfo_x()
        y = root.winfo_y() - root.winfo_height()+118
        
        # Defineix les dimensions i la posició de la nova finestra
        nova_finestra.geometry(f"744x144+{x}+{y}")
        
        # Crear etiqueta per mostrar el recompte de tumbones lliures
        label_total = tk.Label(nova_finestra, text=f"Hi ha {total_lliures} tumbones lliures." , bg="Gold" , font=(button_font, 20))
        label_total.pack(pady=10)
        
        # Crear etiqueta per mostrar els codis de les tumbones lliures
        label_codis = tk.Label(nova_finestra, text=f"Estan lliures: {codis}" , bg="Gold" , font=(button_font, 16))
        label_codis.pack(pady=10)
        
        
        
        # Mostrar la finestra
        nova_finestra.mainloop()

    def consultar_tumbones_lliures():
        try:
            # Connexió a la base de dades
            conn = sqlite3.connect('xiringuito.db')
            cursor = conn.cursor()
            
            # Consulta per obtenir el recompte de tumbones lliures
            cursor.execute('SELECT COUNT(*) FROM Tumbones WHERE estat = "Lliure"')
            total_lliures = cursor.fetchone()[0]

            # Consulta per obtenir el codi de les tumbones lliures
            cursor.execute('SELECT codi FROM Tumbones WHERE estat = "Lliure"')
            codi_lliures = cursor.fetchall()
            codis = ", ".join(str(codi[0]) for codi in codi_lliures)
            
            # Tancar el cursor
            cursor.close()

            # Mostrar la informació en una finestra personalitzada
            mostrar_informacio(total_lliures, codis)
            
        except sqlite3.Error as e:
            print("Error:", e)
            
        finally:
            # Tanquem la connexió
            conn.close()


    def mostrar_dades_usuari():
        permisos_Usuari=obtenir_permisos(username)
        if permisos_Usuari == 'Administrador':

            nova_finestra = tk.Toplevel(root)
            nova_finestra.title("Mostrar Usuari")
            nova_finestra.configure(bg="SteelBlue")
            
            # Calcula les coordenades per centrar la nova finestra respecte a la finestra principal
            x = root.winfo_x()
            y = root.winfo_y() + root.winfo_height() + 32
            
            # Defineix les dimensions i la posició de la nova finestra
            nova_finestra.geometry(f"342x144+{x}+{y}")

            tk.Label(nova_finestra, text="Número de Tumbona:", bg="Gold").grid(row=0, column=0, padx=10, pady=5)
            codi_entry = tk.Entry(nova_finestra)
            codi_entry.grid(row=0, column=1, padx=10, pady=5)

            def mostrar_dades_usuari_inner():
                codi = codi_entry.get()
                try:
                    # Connexió a la base de dades
                    conn = sqlite3.connect('xiringuito.db')
                    cursor = conn.cursor()

                    # Obtenir el DNI de l'usuari que ocupa la butaca a partir de la taula Lloguers
                    cursor.execute('''
                        SELECT Usuaris.dni, Usuaris.nom, Usuaris.telefon 
                        FROM Lloguers 
                        JOIN Usuaris ON Lloguers.Usuari = Usuaris.dni 
                        WHERE Lloguers.Tumbona = ? AND Lloguers.Data_Fi IS NULL
                    ''', (codi,))
                    
                    dades_usuari = cursor.fetchone()

                    if dades_usuari:
                        # Mostrar les dades de l'usuari en una finestra emergent
                        messagebox.showinfo("Dades de l'Usuari", f"DNI: {dades_usuari[0]}\nNom: {dades_usuari[1]}\nTelèfon: {dades_usuari[2]}")
                    else:
                        messagebox.showerror("Error", "Aquesta butaca no està ocupada per cap usuari")

                except sqlite3.Error as e:
                    messagebox.showerror("Error", str(e))

                finally:
                    # Tancar la connexió a la base de dades
                    conn.close()
                    nova_finestra.destroy()  # Tanquem la finestra després de mostrar les dades
        else:
            messagebox.showerror("Accés Denegat", "No tens permisos d'administrador per accedir a aquesta funcionalitat.")

        
        crear_boto(root)
    
        # Mostrar finestra emergent (Mostrar Usuari)
        mostrar_button = tk.Button(nova_finestra, text="Mostrar", width=44, height=5 , bg="Gold" , font=button_font, command=mostrar_dades_usuari_inner)
        mostrar_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    # Mètode per crear el botó per mostrar les dades de l'usuari
    def crear_boto(root):
        mostrar_usuari_button = tk.Button(root, text="Mostrar Usuari", width=20, height=5 , bg="Gold" , font=button_font, command=mostrar_dades_usuari)
        mostrar_usuari_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    # Botó per a llogar una tumbona
    nou_lloguer_button = tk.Button(root, text="Nou Lloguer", width=20, height=5 , bg="Gold" , font=button_font, command=nou_lloguer)
    nou_lloguer_button.grid(row=1, column=2, padx=10, pady=5)

    # Botó per efectuar un cobrament
    cobrar_button = tk.Button(root, text="Cobrar",  width=20, height=5 , bg="Gold" , font=button_font, command=cobrar_lloguer)
    cobrar_button.grid(row=3, column=2, padx=10, pady=5)

    # Botó per consultar el recompte de beneficis
    consultar_button = tk.Button(root, text="Consultar Beneficis", width=44, height=5 , bg="Gold" , font=button_font, command=consultar_beneficis)
    consultar_button.grid(row=5, column=1, columnspan=2, padx=10, pady=5)

    # Botó per consultar el recompte de tumbones lliures
    tumbones_lliures_button = tk.Button(root, text="Tumbones Lliures", width=20, height=5 , bg="Gold" , font=button_font, command=consultar_tumbones_lliures)
    tumbones_lliures_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    # Botó per mostrar les dades d'un client
    mostrar_usuari_button = tk.Button(root, text="Mostrar Usuari", width=20, height=5 , bg="Gold" , font=button_font, command=mostrar_dades_usuari)
    mostrar_usuari_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    

    # Inici de l'aplicació
    root.mainloop()
mostrar_finestra_login()    

