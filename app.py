from flask import Flask, request, jsonify, send_file
from config import get_connection
import csv

app = Flask(__name__)

# ---------------- HOME ----------------

@app.route('/')
def home():
    return send_file('index.html')


# ---------------- ADD PRODUCT ----------------

@app.route('/add-product', methods=['POST'])
def add_product():

    data = request.json

    name = data.get('name')
    sku = data.get('sku')

    if not name or not sku:
        return jsonify({"error": "Name and SKU required"}), 400

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO products (name, sku)
            VALUES (%s, %s)
            RETURNING id
            """,
            (name, sku)
        )

        product_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO inventory (product_id, quantity)
            VALUES (%s, 0)
            """,
            (product_id,)
        )

        conn.commit()

        return jsonify({
            "message": "Product added"
        })

    except Exception as e:

        conn.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()


# ---------------- UPDATE STOCK ----------------

@app.route('/update-stock', methods=['POST'])
def update_stock():

    data = request.json

    product_id = data.get('product_id')
    quantity = data.get('quantity')
    action = data.get('action')

    if not product_id or not quantity or action not in ['IN', 'OUT']:
        return jsonify({
            "error": "Invalid input"
        }), 400

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT quantity
            FROM inventory
            WHERE product_id = %s
            """,
            (product_id,)
        )

        result = cur.fetchone()

        if not result:
            return jsonify({
                "error": "Product not found"
            }), 404

        current_qty = result[0]

        if action == 'IN':

            new_qty = current_qty + quantity

        else:

            if quantity > current_qty:

                return jsonify({
                    "error": "Not enough stock"
                }), 400

            new_qty = current_qty - quantity

        cur.execute(
            """
            UPDATE inventory
            SET quantity = %s
            WHERE product_id = %s
            """,
            (new_qty, product_id)
        )

        cur.execute(
            """
            INSERT INTO transactions
            (product_id, type, quantity)
            VALUES (%s, %s, %s)
            """,
            (product_id, action, quantity)
        )

        conn.commit()

        return jsonify({
            "message": "Stock updated"
        })

    except Exception as e:

        conn.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()


# ---------------- INVENTORY ----------------

@app.route('/inventory', methods=['GET'])
def view_inventory():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                p.id,
                p.name,
                p.sku,
                i.quantity
            FROM products p
            JOIN inventory i
            ON p.id = i.product_id
            ORDER BY p.id
        """)

        rows = cur.fetchall()

        data = []

        for row in rows:

            data.append({

                "id": row[0],
                "name": row[1],
                "sku": row[2],
                "quantity": row[3]

            })

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()


# ---------------- TRANSACTIONS ----------------

@app.route('/transactions', methods=['GET'])
def get_transactions():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                t.id,
                p.name,
                t.type,
                t.quantity,
                TO_CHAR(
                    t.created_at,
                    'DD-MM-YYYY HH24:MI:SS'
                )
            FROM transactions t
            JOIN products p
            ON t.product_id = p.id
            ORDER BY t.created_at DESC
        """)

        rows = cur.fetchall()

        data = []

        for row in rows:

            data.append({

                "transaction_id": row[0],
                "product_name": row[1],
                "type": row[2],
                "quantity": row[3],
                "time": row[4]

            })

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()


# ---------------- DELETE PRODUCT ----------------

@app.route('/delete-product/<int:id>', methods=['DELETE'])
def delete_product(id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            "DELETE FROM transactions WHERE product_id = %s",
            (id,)
        )

        cur.execute(
            "DELETE FROM inventory WHERE product_id = %s",
            (id,)
        )

        cur.execute(
            "DELETE FROM products WHERE id = %s",
            (id,)
        )

        conn.commit()

        return jsonify({
            "message": "Product deleted"
        })

    except Exception as e:

        conn.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()


# ---------------- RESET DATABASE ----------------

@app.route('/reset', methods=['POST'])
def reset_database():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("DELETE FROM transactions")
        cur.execute("DELETE FROM inventory")
        cur.execute("DELETE FROM products")

        conn.commit()

        return jsonify({
            "message": "Database reset successful"
        })

    except Exception as e:

        conn.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()


# ---------------- EXPORT INVENTORY CSV ----------------

@app.route('/export-inventory')
def export_inventory():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.name,
            p.sku,
            i.quantity
        FROM products p
        JOIN inventory i
        ON p.id = i.product_id
        ORDER BY p.name
    """)

    rows = cur.fetchall()

    with open(
        'inventory_report.csv',
        'w',
        newline=''
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            'Product Name',
            'SKU',
            'Quantity'
        ])

        writer.writerows(rows)

    cur.close()
    conn.close()

    return send_file(
        'inventory_report.csv',
        as_attachment=True
    )


# ---------------- EXPORT TRANSACTIONS CSV ----------------

@app.route('/export-transactions')
def export_transactions():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.name,
            t.type,
            t.quantity,
            TO_CHAR(
                t.created_at,
                'DD-MM-YYYY HH24:MI:SS'
            )
        FROM transactions t
        JOIN products p
        ON t.product_id = p.id
        ORDER BY t.created_at DESC
    """)

    rows = cur.fetchall()

    with open(
        'transactions_report.csv',
        'w',
        newline=''
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            'Product Name',
            'Type',
            'Quantity',
            'Time'
        ])

        writer.writerows(rows)

    cur.close()
    conn.close()

    return send_file(
        'transactions_report.csv',
        as_attachment=True
    )


# ---------------- RUN APP ----------------

if __name__ == '__main__':
    app.run(debug=True)