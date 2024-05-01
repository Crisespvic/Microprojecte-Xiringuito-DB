import sqlite3

def crear_bd():
    try:
        # Conexió a la base de dades (crea l'arxiu si no existeix)
        conn = sqlite3.connect('xiringuito.db')
        cursor = conn.cursor()
        
        # Crea la taula Usuaris (si no existeix)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuaris (
                Dni VARCHAR(9) PRIMARY KEY,
                Nom VARCHAR(30),
                Telefon INT
            )
        ''')
        
        # Crea la taula Tumbones (si no existeix)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Tumbones (
                Codi INT PRIMARY KEY,
                Estat VARCHAR(10) NOT NULL,
                Preu DECIMAL(6,2)
            )
        ''')

         # Crea la taula Lloguers (si no existeix)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Lloguers (
                id INTEGER PRIMARY KEY,
                Usuari VARCHAR(9) NOT NULL,
                Tumbona INT NOT NULL,       
                Data_Inici TIMESTAMP DEFAULT NULL,
                Data_Fi TIMESTAMP DEFAULT NULL,
                FOREIGN KEY(Usuari) REFERENCES Usuaris(dni),
                FOREIGN KEY(Tumbona) REFERENCES Tumbones(codi)
            )
        ''')

        # Crea la taula Users (si no existeix)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                Id INTEGER PRIMARY KEY,
                NomUsuari VARCHAR(30) UNIQUE,
                Contrasenya VARCHAR(30),
                Permisos VARCHAR(30)
            )
        ''')
        
        # Inserta els usuaris inicials (admin i usuari) amb les seves contrasenyes i permisos
        cursor.execute('INSERT OR IGNORE INTO Users (NomUsuari, Contrasenya, Permisos) VALUES (?, ?, ?)', ('admin', '1234', 'Administrador'))
        cursor.execute('INSERT OR IGNORE INTO Users (NomUsuari, Contrasenya, Permisos) VALUES (?, ?, ?)', ('user', '0000', 'Usuari'))
        
        # Comfirma els canvis en la base de dades
        conn.commit()
        print("Base de dades i taules creades correctament.")
    # Error al crear la base de dades     
    except sqlite3.Error as e:
        print("Error al crear la base de dades:", e)
        
    finally:
        # Tancar la conexió a la base de datos
        if conn:
            conn.close()

def insertar_tumbones_inicials():
    try:
        # Conexió a la base de dades
        conn = sqlite3.connect('xiringuito.db')
        cursor = conn.cursor()

        # Inserta 20 tumbones amb estat "Lliure" i preu 40€
        for i in range(1, 21):
            cursor.execute('INSERT INTO Tumbones (codi, estat, preu) VALUES (?, ?, ?)', (i, 'Lliure', 40))

        # Confirma els canvis en la base de dades
        conn.commit()
        print("S'han insertat les tumbones inicials correctament.")
    # Error al fer el insert de tumbones    
    except sqlite3.Error as e:
        print("Error al insertar les tumbones inicials:", e)
        
    finally:
        # Tancar la conexió a la base de dades
        if conn:
            conn.close()

# Función per a crear la base de dades amb les taules
crear_bd()
# Función per a insertar les tumbonas inicials
insertar_tumbones_inicials()