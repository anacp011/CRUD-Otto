DROP DATABASE IF EXISTS KrauseBBDD;
CREATE DATABASE KrauseBBDD;

USE KrauseBBDD;

CREATE TABLE proveedores (
 ID_Provee INT AUTO_INCREMENT PRIMARY KEY,
 nroProvee INT UNIQUE NOT NULL,
 nombre VARCHAR(100) NOT NULL,
 contacto VARCHAR(100)
);

CREATE TABLE materias_primas (
 ID_MatPrim INT AUTO_INCREMENT PRIMARY KEY,
 nroMatPrim INT UNIQUE NOT NULL,
 nombre VARCHAR(100) NOT NULL,
 cantidad VARCHAR NOT NULL,
 proveedor_id INT,
 FOREIGN KEY (proveedor_id) REFERENCES proveedores(ID_Provee)
);

CREATE TABLE etiquetas (
 ID_Etiquetas INT AUTO_INCREMENT PRIMARY KEY,
 nroEtiquetas INT UNIQUE NOT NULL,
 nombre VARCHAR(100) NOT NULL,
 proveedor_id INT,
 FOREIGN KEY (proveedor_id) REFERENCES proveedores(ID_Provee)
);

CREATE TABLE envases (
 ID_Envases INT AUTO_INCREMENT PRIMARY KEY,
 nroEnvases INT UNIQUE NOT NULL,
 nombre VARCHAR(100) NOT NULL,
 proveedor_id INT,
 FOREIGN KEY (proveedor_id) REFERENCES proveedores(ID_Provee)
);

CREATE TABLE lotes (
 ID_Lotes INT AUTO_INCREMENT PRIMARY KEY,
 nroLotes INT UNIQUE NOT NULL,
 fecha_inicio DATE NOT NULL,
 fecha_fin DATE,
 cantidad INT NOT NULL
);

CREATE TABLE productos_finales (
 ID_ProdF INT AUTO_INCREMENT PRIMARY KEY,
 nroProdF INT UNIQUE NOT NULL,
 nombre VARCHAR(100) NOT NULL,
 lote_id INT,
 cantidad INT NOT NULL,
 FOREIGN KEY (lote_id) REFERENCES lotes(ID_Lotes)
);

CREATE TABLE productos_cuarentena (
 ID_ProdC INT AUTO_INCREMENT PRIMARY KEY,
 nroProdC INT UNIQUE NOT NULL,
 producto_id INT,
 FOREIGN KEY (producto_id) REFERENCES productos_finales(ID_ProdF)
);

CREATE TABLE productos_descarte (
 ID_ProdD INT AUTO_INCREMENT PRIMARY KEY,
 nroProdD INT UNIQUE NOT NULL,
 producto_id INT,
 FOREIGN KEY (producto_id) REFERENCES productos_finales(ID_ProdF)
);