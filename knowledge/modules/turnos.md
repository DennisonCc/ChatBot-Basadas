## 📅 Módulo de Turnos y Horarios

> 🔗 **Depende de:** [personal.md](./personal.md) (empleados)  
> 🔗 **Input para:** [asistencia.md](./asistencia.md) (marcaciones)  
> 🔙 **Volver:** [main.md](../main.md)

Gestiona la planificación del tiempo laboral de los colaboradores.

### Funciones Principales
- Creación de turnos (Rotativos, Fijos).
- Asignación de horarios semanales.
- Cálculo automático de horas totales.

### Campos del Turno
| Campo | Descripción |
|-------|-------------|
| Hora inicio / Hora fin | Rango de 07:00 a 20:30 |
| Total horas | Calculado automáticamente |
| Nombre | Identificador del turno |
| Tipo | NORMAL, ADICIONAL |

### Validaciones
- La hora final no puede ser inferior a la hora inicial.
- Todos los campos son obligatorios.

### Soporte Común
- Las horas impactan directamente en el cálculo de horas extras.
- Los cambios de turno deben realizarse con antelación.

*Estado de API: En desarrollo*

---
**Ver detalles UI:** [Pantallas → Turnos](./pantallas.md#-pantalla-de-turnos-turnojava)
