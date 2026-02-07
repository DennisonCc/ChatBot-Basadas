## 🖥️ Pantallas del Sistema de Gestión de Personal (Java Swing)

Este documento describe todas las pantallas (vistas) del sistema de gestión de personal desarrollado en Java Swing.

---

### 🔐 Pantalla de Login (`Login.java`)

Pantalla inicial de autenticación del sistema.

- **Funciones**:
  - Autenticación de usuarios con usuario y contraseña.
  - Validación de credenciales contra la base de datos.
  - Redirección a la pantalla Base tras login exitoso.
- **Campos**:
  - Usuario (campo de texto)
  - Contraseña (campo de contraseña)
- **Acciones**:
  - Botón "Ingresar": Valida credenciales y accede al sistema.
- **Mensajes de Error Comunes**:
  - "Faltan datos de usuario y contraseña" - Cuando algún campo está vacío.
  - "El usuario no existe" - Cuando las credenciales son incorrectas.

---

### 🏠 Pantalla Base (`Base.java`)

Ventana principal MDI (Multiple Document Interface) que contiene el menú de navegación.

- **Menús**:
  - **Ingresar**:
    - Personal
    - Turnos
    - Recesos
    - Tiempos fuera de trabajo
  - **Reportes**:
    - Jornada total
    - Pausas y visitas
- **Características**:
  - Escritorio (JDesktopPane) para alojar ventanas internas.
  - Almacena el usuario logueado en variable estática `Base.usuario`.

---

### 👥 Pantalla de Personal (`Personal.java`)

Gestión completa de empleados del sistema.

- **Funciones Principales**:
  - Registro de nuevos empleados.
  - Actualización de datos de empleados existentes.
  - Búsqueda de empleados por nombre o apellido.
  - Listado de todos los empleados en tabla.
- **Campos del Formulario** (Detalle Absoluto):
  - **Identificación**: CI (PK), Nombres, Apellidos.
  - **Ubicación**: Dirección (TextArea), Teléfonos, Correo.
  - **Fechas**: Nacimiento, Ingreso, Contrato (JDateChooser).
  - **Finanzas**: Salario (Double).
  - **Selectores Dinámicos**: Área (ID_A), Turno (ID_T), Break (ID_B), Almuerzo (ID_BA).
- **Lógica Crítica**:
  - **Normalización**: Todos los campos de texto se convierten automáticamente a **MAYÚSCULAS** al guardar.
  - **Cascade**: Al cambiar el Turno, los selectores de Break y Almuerzo se limpian y recargan filtrando solo los recesos asociados a ese turno específico.
  - **Persistencia**: La acción "Guardar" utiliza `Personals_modelo.guardar` que decide entre INSERT o UPDATE basándose en si existe un ID previo.
- **Soporte Común**:
  - Para actualizar un registro, se debe seleccionar primero en la tabla superior (evento `mouseClicked`).

---

### 🏢 Gestión de Áreas (`modelos/Areas.java`)

Aunque no tiene una pantalla visual independiente en el menú principal, las áreas son entidades fundamentales gestionadas en la base de datos (tabla `area`).

- **Campos**:
  - `ID_A`: Identificador único (PK).
  - `NOMBRE`: Nombre del departamento o área.
  - `DESCRIPCION`: Detalles del área.
- **Relación**: Cada empleado debe estar vinculado a un `ID_A`.

---

### 📅 Pantalla de Turnos (`Turno.java`)

Gestión de turnos laborales.

- **Funciones Principales**:
  - Creación de turnos de trabajo.
  - Cálculo automático de horas totales.
  - Búsqueda de turnos por nombre.
- **Campos del Formulario**:
  - Hora inicio (ComboBox con horas de 07:00 a 20:30)
  - Hora fin (ComboBox con horas de 07:00 a 20:30)
  - Total de horas (calculado automáticamente)
  - Nombre del turno
  - Descripción
  - Tipo (NORMAL, ADICIONAL)
- **Tabla de Turnos** (7 columnas):
  - ID, Hora inicio, Hora fin, Total, Nombre, Descripción, Tipo
- **Validaciones**:
  - La hora final no puede ser inferior a la hora inicial.
  - Todos los campos son obligatorios.
- **Soporte Común**:
  - Los turnos impactan directamente en el cálculo de horas extras.
  - Los cambios de turno deben realizarse con antelación.

---

### ☕ Pantalla de Recesos (`Receso.java`)

Gestión de breaks y almuerzos asociados a turnos.

- **Funciones Principales**:
  - Creación de recesos (breaks y almuerzos).
  - Asociación de recesos a turnos específicos.
  - Búsqueda de recesos por nombre.
- **Campos del Formulario**:
  - Turno asociado (ComboBox dinámico)
  - Tipo de receso (BREAK, ALMUERZO)
  - Nombre del receso
  - Hora de inicio (ComboBox)
  - Tiempo/Duración del receso (15min, 30min, 45min, 1h)
  - Total de tiempo (calculado)
  - Descripción
- **Tabla de Recesos** (8 columnas):
  - ID, Hora inicio, Duración, Total, Nombre, Descripción, Turno, Tipo
- **Validaciones**:
  - El tipo de receso es obligatorio.
  - Debe seleccionarse hora de inicio.
  - Debe seleccionarse el rango/duración.
  - Nombre y descripción son obligatorios.

---

### ⏸️ Pantalla de Pausas Activas (`PausasActivas.java`)

Registro de tiempos fuera de trabajo programados (capacitaciones, permisos, reuniones).

- **Funciones Principales**:
  - Registro de pausas activas para múltiples empleados simultáneamente.
  - Gestión de diferentes tipos de pausas.
- **Tipos de Pausas y Sub-estados**:
  - **Capacitación**: C_interna, C_externa
  - **No ready**: NR_baño_agua
  - **Permisos**: P_con_descuento, P_sin_descuento
  - **Reunión**: R_interna, R_externa
  - **Visita**: V_clientes, V_proveedores
- **Lógica de Batch**:
  - El panel de empleados carga una lista de **JCheckBox** generada dinámicamente desde la tabla `empleado`.
  - Se puede asignar una misma pausa a N empleados en una sola transacción.
- **Validaciones Técnicas**:
  - `verificar_hora_inicio_fin`: Compara la primera parte de la cadena `HH:mm` para asegurar que el fin no sea cronológicamente anterior al inicio.
  - Observaciones: Convertidas a MAYÚSCULAS.
- **Acciones**:
  - Botón "Guardar": Itera sobre el array `campos[]` y ejecuta `lm.guardar_pausas` por cada check marcado.
  - Botón "Limpiar": Resetea el formulario y recarga la lista de empleados.

---

### 🚶 Pantalla de Pausas y Visitas (`PausasVisitas.java`)

Registro rápido de pausas y visitas con firma del empleado.

- **Funciones Principales**:
  - Registro de pausas rápidas (baño, agua).
  - Registro de visitas (clientes, proveedores).
  - Sistema de firma para entrada/salida de pausas.
- **Tipos y Sub-tipos**:
  - **No ready**: NR_agua_baño
  - **Visita**: V_clientes, V_proveedores
- **Campos del Formulario**:
  - Tipo de pausa
  - Sub tipo
  - Observación
  - Firma (identificador del empleado)
- **Lógica de Funcionamiento**:
  - Primera firma: Registra inicio de pausa.
  - Segunda firma (mismo día, mismo tipo): Registra fin de pausa.
- **Mensajes**:
  - "El empleado no existe" - Cuando la firma no corresponde a un CI válido.
  - "Registro almacenado" - Confirmación de operación exitosa.

---

### 📊 Pantalla de Reporte Jornada Total (`JornadaTotal.java`)

Reporte detallado de jornadas laborales de empleados.

- **Funciones Principales**:
  - Consulta de jornadas por rango de fechas.
  - Filtro por empleado o todos.
  - Exportación a Excel.
- **Filtros**:
  - Fecha inicio
  - Fecha fin
  - Empleado (ComboBox con opción "Todos")
- **Columnas del Reporte** (14 columnas):
  - CI, Fecha Firma, Nombres, Apellidos, Ingreso Jornada, Salida Jornada, Inicio Break, Regreso Break, Inicio Almuerzo, Regreso Almuerzo, Atraso Jornada, Atraso Break, Atraso Almuerzo, Observaciones
- **Acciones**:
  - Botón "Consultar": Ejecuta la consulta con los filtros.
  - Botón "Exportar": Genera archivo Excel (.xls).

---

### 📋 Pantalla de Reporte Pausas y Visitas (`PausasVisitasReporte.java`)

Reporte detallado de pausas y visitas registradas.

- **Funciones Principales**:
  - Consulta de pausas por rango de fechas.
  - Filtro por empleado o todos.
  - Exportación a Excel.
- **Filtros**:
  - Fecha inicio
  - Fecha fin
  - Empleado (ComboBox con opción "Todos")
- **Columnas del Reporte** (11 columnas):
  - Tipo, Sub Tipo, Nombres, Apellidos, CI, Observación, Fecha, Hora Inicio, Hora Fin, Fecha Edición, Usuario Edición
- **Acciones**:
  - Botón "Consultar": Ejecuta la consulta con los filtros.
  - Botón "Exportar": Genera archivo Excel (.xls).

---

### ✍️ Pantalla Base de Firma (`BaseFirma.java`)

Sistema de marcaje/fichaje de asistencia con cronómetro integrado.

- **Funciones Principales**:
  - Registro de ingreso a jornada.
  - Registro de inicio/fin de break con cronómetro.
  - Registro de inicio/fin de almuerzo con cronómetro.
  - Registro de salida de jornada.
  - Cálculo automático de atrasos.
  - Auto-completado de firmas no realizadas del día anterior.
- **Campos de Visualización**:
  - Empleado
  - Ingreso de jornada + Atraso
  - Salida al break + Cronómetro break
  - Regreso del break + Atraso
  - Salida al almuerzo + Cronómetro almuerzo
  - Regreso del almuerzo + Atraso
  - Salida de jornada
- **Campo de Entrada**:
  - Firma (CI del empleado)
- **Lógica de Funcionamiento** (Secuencia Absoluta):
  1. **Firma 1**: Ingreso Jornada (Cálculo de atraso vs Turno).
  2. **Firma 2**: Salida Break (Inicia hilo `hilo`).
  3. **Firma 3**: Regreso Break (Suspende `hilo`, calcula exceso).
  4. **Firma 4**: Salida Almuerzo (Inicia hilo `hilo_almuerzo`).
  5. **Firma 5**: Regreso Almuerzo (Suspende `hilo_almuerzo`, calcula exceso).
  6. **Firma 6**: Salida Jornada.
- **Auto-completado Inteligente (`actualizar_no_firmas`)**:
  - Al iniciar la ventana, el sistema busca firmas incompletas de días previos.
  - Si falta alguna firma de la secuencia, auto-completa los campos restantes con la **Hora de Fin de Turno** oficial y añade una observación técnica automática.
- **Componentes Técnicos**:
  - Usa hilos (`Thread`) para actualizar los campos `c_bjTextField` y `c_ajTextField` cada 10ms (precisión de decisegundos).

---

Las pantallas utilizan los siguientes modelos y tablas de base de datos:

| Modelo (Java) | Tabla (PostgreSQL) | Descripción | Campos Clave |
|--------|-------------|-------------|--------------|
| `Personals` | `empleado` | Datos del personal | `CI` (PK), `ID_A`, `ID_T`, `ID_B`, `ID_BA` |
| `Turnos` | `turno` | Planificación | `ID_T` (PK), `H_INC`, `H_FIN`, `TOTAL`, `TIPO` |
| `Recesos` | `receso` | Breaks/Almuerzos | `ID_R` (PK), `ID_T` (FK), `DURACION`, `TIPO` |
| `Firmas` | `firmas` | Asistencia diaria | `ID_F` (PK), `CI` (FK), `FECHA`, `ING_JORNADA` |
| `Areas` | `area` | Departamentos | `ID_A` (PK), `NOMBRE` |
| `Login` | `usuario` | Seguridad | `ID_U`, `USUARIO`, `CLAVE` |
| `Pausas` | `tiempofuera` | Pausas activas | `ID_P`, `CI`, `FECHA`, `H_INC`, `H_FIN` |

---

## 🔗 Flujo de Navegación

```
Login
  └── Base (MDI Principal)
       ├── Menú Ingresar
       │    ├── Personal
       │    ├── Turnos
       │    ├── Recesos
       │    └── PausasActivas (Tiempos fuera)
       └── Menú Reportes
            ├── JornadaTotal
            └── PausasVisitasReporte

BaseFirma (Pantalla independiente para terminales de fichaje)
  └── Menú
       ├── Personal
       └── PausasVisitas
```

---

## ⚠️ Problemas Comunes y Soluciones

| Problema | Solución |
|----------|----------|
| El empleado no aparece en listas | Verificar que esté **Activo** en módulo Personal |
| No cargan los breaks/almuerzos | Verificar que el turno tenga recesos configurados |
| Error al guardar empleado | Verificar que todos los campos obligatorios estén completos |
| Atrasos incorrectos | Revisar configuración de hora de inicio del turno |
| Cronómetro no se detiene | Realizar la siguiente firma en secuencia |
| Reporte vacío | Verificar rango de fechas y que existan registros |

*Estado de API Backend: Conectado (Básico)*
