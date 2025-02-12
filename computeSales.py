import sys
import json
import time
import os


def read_json_file(filename):
    """Lee un archivo JSON y retorna su contenido."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al leer {filename}: {e}")
        return None


def create_price_dict(price_catalogue):
    """Convierte la lista de productos en un diccionario con precios."""
    price_dict = {}
    for item in price_catalogue:
        product_name = item.get("title")
        price = item.get("price")
        if product_name and isinstance(price, (int, float)):
            price_dict[product_name] = price
    return price_dict


def compute_total_sales(price_catalogue, sales_record):
    """Calcula el costo total de las ventas basándose en el catálogo de precios."""
    price_dict = create_price_dict(price_catalogue)
    total_sales = 0
    errors = []
    
    for sale in sales_record:
        product = sale.get("Product")  # Se ajusta para coincidir con el formato del JSON
        quantity = sale.get("Quantity")
        
        if product not in price_dict:
            errors.append(f"Producto no encontrado: {product}")
            continue
        
        if not isinstance(quantity, (int, float)) or quantity < 0:
            errors.append(f"Cantidad inválida para {product}: {quantity}")
            continue
        
        total_sales += price_dict[product] * quantity
    
    return total_sales, errors


def write_results(filename, total_sales, elapsed_time, errors):
    """Escribe los resultados en un archivo de texto."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Costo total de ventas: {total_sales:.2f}\n")
        file.write(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos\n")
        if errors:
            file.write("Errores encontrados:\n")
            for error in errors:
                file.write(f"- {error}\n")


def run_flake8():
    """Ejecuta Flake8 y guarda el reporte en un archivo."""
    flake8_report = "flake8_report.txt"
    command = "py -3.9 -m flake8 computeSales.py --max-line-length=100 > flake8_report.txt"
    os.system(command)
    print(f"Reporte de Flake8 generado en {flake8_report}")


def main():
    """Función principal que lee archivos JSON, calcula ventas y muestra los resultados."""
    if len(sys.argv) > 1 and sys.argv[1] == "--lint":
        run_flake8()
        sys.exit(0)

    if len(sys.argv) != 3:
        print("Uso: python computeSales.py priceCatalogue.json salesRecord.json")
        sys.exit(1)

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]
    output_filename = "SalesResults.txt"

    start_time = time.time()
    price_catalogue = read_json_file(price_catalogue_file)
    sales_record = read_json_file(sales_record_file)

    if price_catalogue is None or sales_record is None:
        print("No se pudo leer uno o ambos archivos JSON.")
        sys.exit(1)

    total_sales, errors = compute_total_sales(price_catalogue, sales_record)
    elapsed_time = time.time() - start_time

    print(f"Costo total de ventas: {total_sales:.2f}")
    print(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos")
    if errors:
        print("Errores encontrados:")
        for error in errors:
            print(f"- {error}")

    write_results(output_filename, total_sales, elapsed_time, errors)


if __name__ == "__main__":
    main()
