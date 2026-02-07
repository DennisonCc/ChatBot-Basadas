## ☕ Módulo de Tiempos Fuera

> 🔗 **Depende de:** [personal.md](./personal.md) (empleados)  
> 🔙 **Volver:** [main.md](../main.md)

Gestión de pausas activas. Incluye soporte para traslapes, olvidos de cierre y errores en tipo de pausa.

### ¿Qué hace el módulo?
- **Agregar Pausa**: Registra una nueva pausa activa para un empleado.
- **Actualizar Pausa**: Modifica detalles de una pausa existente.

### Tipos de Pausas y Sub-estados
| Tipo | Sub-estados |
|------|-------------|
| Capacitación | C_interna, C_externa |
| No ready | NR_baño_agua |
| Permisos | P_con_descuento, P_sin_descuento |
| Reunión | R_interna, R_externa |
| Visita | V_clientes, V_proveedores |

### ¿Qué pasa si no carga el módulo?
1. Verificar conexión a la base de datos.
2. Reiniciar la aplicación.
3. Contactar soporte técnico si persiste.

*Estado de API: Conectado (Básico)*

---
**Ver detalles UI:** [Pantallas → Pausas Activas](./pantallas.md#️-pantalla-de-pausas-activas-pausasactivasjava)
