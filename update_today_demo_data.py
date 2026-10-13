import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from datetime import datetime, date
from app import create_app
from models import db, User, Product, Sale, SaleDetail, SalePayment, Expense

def populate_today_data():
    app = create_app()
    with app.app_context():
        print("🌱 Sincronizando datos de ventas y gastos de HOY (13 de Octubre de 2026)...")

        admin = User.query.filter_by(rol='admin').first()
        vendedor = User.query.filter_by(rol='vendedor').first() or admin

        # Obtener productos
        p_case_sil = Product.query.filter_by(sku="CASE-IP15P-SIL").first()
        p_case_mag = Product.query.filter_by(sku="CASE-MAGSAFE-CLR").first()
        p_case_arm = Product.query.filter_by(sku="CASE-S24U-ARM").first()
        p_prot_diam = Product.query.filter_by(sku="PROT-CAM-DIAM").first()
        p_vid_cer = Product.query.filter_by(sku="VID-CER-9D-MAT").first()
        p_vid_priv = Product.query.filter_by(sku="VID-PRIV-ESP").first()
        p_carg_25w = Product.query.filter_by(sku="CARG-25W-PD").first()
        p_cab_tren = Product.query.filter_by(sku="CAB-TREN-15M").first()
        p_pop_mag = Product.query.filter_by(sku="POP-MAG-GLIT").first()
        p_lanyard = Product.query.filter_by(sku="LANYARD-LUX").first()
        p_tws_pro = Product.query.filter_by(sku="AUD-TWS-PRO").first()

        # Limpiar ventas de prueba anteriores para reconstruirlas de manera perfecta
        SaleDetail.query.delete()
        SalePayment.query.delete()
        Sale.query.delete()
        db.session.commit()

        def add_sale(vendedor_obj, fecha_dt, monto_tot, metodo_prin, detalles_list, pagos_list=None):
            s = Sale(
                vendedor_id=vendedor_obj.id,
                fecha_venta=fecha_dt,
                monto_total=monto_tot,
                metodo_pago=metodo_prin
            )
            db.session.add(s)
            db.session.flush()

            for det in detalles_list:
                sd = SaleDetail(
                    sale_id=s.id,
                    product_id=det["product"].id if det.get("product") else None,
                    cantidad_vendida=det.get("cantidad", 1),
                    precio_venta_final=det.get("precio", 0)
                )
                db.session.add(sd)

            if pagos_list:
                for pag in pagos_list:
                    sp = SalePayment(
                        sale_id=s.id,
                        metodo_pago=pag["metodo"],
                        monto=pag["monto"]
                    )
                    db.session.add(sp)
            else:
                sp = SalePayment(
                    sale_id=s.id,
                    metodo_pago=metodo_prin,
                    monto=monto_tot
                )
                db.session.add(sp)
            return s

        # --- VENTAS DE HOY (13 DE OCTUBRE DE 2026) ---
        # 1. Venta Efectivo: 2x Case Silicona Matte iPhone 15 Pro
        add_sale(
            vendedor,
            datetime(2026, 10, 13, 9, 30),
            90000,
            "efectivo",
            [{"product": p_case_sil, "cantidad": 2, "precio": 45000}]
        )

        # 2. Venta Nequi: 1x Case Clear MagSafe + 1x Protector Diamante
        add_sale(
            vendedor,
            datetime(2026, 10, 13, 10, 45),
            80000,
            "nequi",
            [
                {"product": p_case_mag, "cantidad": 1, "precio": 55000},
                {"product": p_prot_diam, "cantidad": 1, "precio": 25000}
            ]
        )

        # 3. Venta Bold: 1x Cargador 25W Type-C + 1x Cable Trenzado Reforzado
        add_sale(
            admin,
            datetime(2026, 10, 13, 11, 20),
            93000,
            "bolt",
            [
                {"product": p_carg_25w, "cantidad": 1, "precio": 65000},
                {"product": p_cab_tren, "cantidad": 1, "precio": 28000}
            ]
        )

        # 4. Venta Mixta (Efectivo $50.000 + Nequi $40.000): Audífonos TWS Pro + PopSocket
        add_sale(
            vendedor,
            datetime(2026, 10, 13, 12, 15),
            90000,
            "mixto",
            [
                {"product": p_tws_pro, "cantidad": 1, "precio": 75000},
                {"product": p_pop_mag, "cantidad": 1, "precio": 15000}
            ],
            [
                {"metodo": "efectivo", "monto": 50000},
                {"metodo": "nequi", "monto": 40000}
            ]
        )

        # 5. Venta Bold: 2x Vidrio Privacidad Anti-Espía + 1x PopSocket
        add_sale(
            vendedor,
            datetime(2026, 10, 13, 14, 10),
            59000,
            "bolt",
            [
                {"product": p_vid_priv, "cantidad": 2, "precio": 22000},
                {"product": p_pop_mag, "cantidad": 1, "precio": 15000}
            ]
        )

        # 6. Venta Mixta (Efectivo $40.000 + Bold $33.000): Case Silicona + Cable
        add_sale(
            admin,
            datetime(2026, 10, 13, 15, 30),
            73000,
            "mixto",
            [
                {"product": p_case_sil, "cantidad": 1, "precio": 45000},
                {"product": p_cab_tren, "cantidad": 1, "precio": 28000}
            ],
            [
                {"metodo": "efectivo", "monto": 40000},
                {"metodo": "bolt", "monto": 33000}
            ]
        )

        # 7. Venta Efectivo: 1x Case Armor S24 Ultra + 1x Vidrio Cerámico 9D
        add_sale(
            vendedor,
            datetime(2026, 10, 13, 16, 20),
            68000,
            "efectivo",
            [
                {"product": p_case_arm, "cantidad": 1, "precio": 50000},
                {"product": p_vid_cer, "cantidad": 1, "precio": 18000}
            ]
        )

        # 8. Venta Nequi: 2x Correa Lanyard Luxury + 1x Protector Diamante
        add_sale(
            vendedor,
            datetime(2026, 10, 13, 16, 50),
            65000,
            "nequi",
            [
                {"product": p_lanyard, "cantidad": 2, "precio": 20000},
                {"product": p_prot_diam, "cantidad": 1, "precio": 25000}
            ]
        )

        # --- VENTAS DE DÍAS ANTERIORES EN OCTUBRE 2026 ---
        add_sale(
            vendedor,
            datetime(2026, 10, 5, 11, 0),
            110000,
            "efectivo",
            [{"product": p_carg_25w, "cantidad": 1, "precio": 65000}, {"product": p_case_sil, "cantidad": 1, "precio": 45000}]
        )
        add_sale(
            admin,
            datetime(2026, 10, 8, 14, 30),
            120000,
            "nequi",
            [{"product": p_case_mag, "cantidad": 2, "precio": 55000}, {"product": p_pop_mag, "cantidad": 1, "precio": 10000}]
        )
        add_sale(
            vendedor,
            datetime(2026, 10, 10, 16, 0),
            95000,
            "bolt",
            [{"product": p_tws_pro, "cantidad": 1, "precio": 75000}, {"product": p_lanyard, "cantidad": 1, "precio": 20000}]
        )
        add_sale(
            vendedor,
            datetime(2026, 10, 12, 17, 30),
            100000,
            "efectivo",
            [{"product": p_case_arm, "cantidad": 2, "precio": 50000}]
        )

        # --- GASTOS DE HOY (13 DE OCTUBRE DE 2026) ---
        # Limpiar y regenerar gastos
        Expense.query.delete()
        db.session.commit()

        gastos_def = [
            # Gastos de Hoy (13 Octubre)
            {
                "tipo": "Gasto Diario",
                "categoria": "Alimentación / Refrigerios",
                "descripcion": "Refrigerios y café equipo de apertura",
                "monto": 35000,
                "metodo": "efectivo",
                "fecha": datetime(2026, 10, 13, 10, 0)
            },
            {
                "tipo": "Gasto Diario",
                "categoria": "Transporte / Domicilios",
                "descripcion": "Mensajería entrega urgente de accesorios cliente VIP",
                "monto": 25000,
                "metodo": "nequi",
                "fecha": datetime(2026, 10, 13, 12, 30)
            },
            {
                "tipo": "Gasto Diario",
                "categoria": "Papelería e Insumos",
                "descripcion": "Rollos térmicos para datáfono y etiquetas adhesivas",
                "monto": 45000,
                "metodo": "bolt",
                "fecha": datetime(2026, 10, 13, 14, 0)
            },
            # Gastos del mes anteriores
            {
                "tipo": "Gasto Diario",
                "categoria": "Empaques y Bolsas",
                "descripcion": "Lote x100 bolsas boutique My Case rosa neón",
                "monto": 120000,
                "metodo": "nequi",
                "fecha": datetime(2026, 10, 5, 14, 30)
            },
            {
                "tipo": "Costo Indirecto",
                "categoria": "Servicios Públicos",
                "descripcion": "Plan comercial internet fibra óptica y telefonía",
                "monto": 115000,
                "metodo": "bolt",
                "fecha": datetime(2026, 10, 7, 10, 0)
            },
            {
                "tipo": "Costo Indirecto",
                "categoria": "Publicidad y Marketing",
                "descripcion": "Campaña publicitaria Instagram Reels y TikTok",
                "monto": 80000,
                "metodo": "bolt",
                "fecha": datetime(2026, 10, 11, 15, 0)
            }
        ]

        for g in gastos_def:
            exp = Expense(
                usuario_id=admin.id,
                tipo_gasto=g["tipo"],
                categoria=g["categoria"],
                descripcion=g["descripcion"],
                monto=g["monto"],
                metodo_pago=g["metodo"],
                fecha_gasto=g["fecha"]
            )
            db.session.add(exp)

        db.session.commit()
        print("✅ Base de datos actualizada con 8 ventas y 3 gastos para el día de HOY (13 de Octubre de 2026) en Efectivo, Nequi y Bold.")

if __name__ == '__main__':
    populate_today_data()
