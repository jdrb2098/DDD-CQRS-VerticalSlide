# Frontend - Asisya Application

## Documentación para Desarrolladores Backend

Esta documentación está diseñada para ayudar a desarrolladores backend a entender la arquitectura y funcionamiento del frontend de la aplicación Asisya durante entrevistas técnicas o revisiones de código.

---

## 📋 Tabla de Contenidos

1. [Arquitectura General](#arquitectura-general)
2. [Stack Tecnológico](#stack-tecnológico)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Autenticación y Autorización](#autenticación-y-autorización)
5. [Comunicación con la API](#comunicación-con-la-api)
6. [Enrutamiento](#enrutamiento)
7. [Formularios y Validación](#formularios-y-validación)
8. [Gestión de Estado](#gestión-de-estado)
9. [Puntos Clave para la Entrevista](#puntos-clave-para-la-entrevista)

---

## 🏗️ Arquitectura General

El frontend es una **Single Page Application (SPA)** construida con React y TypeScript. Utiliza una arquitectura modular basada en:

- **Componentes funcionales** con hooks de React
- **Separación de responsabilidades**: servicios, contextos, componentes y páginas
- **TypeScript estricto** para type safety en toda la aplicación
- **Interceptores HTTP** para manejo automático de tokens y errores

### Flujo de la Aplicación

```
Usuario → Login → Obtiene JWT → Guarda en localStorage →
Interceptor agrega token a requests → AuthGuard protege rutas →
Componentes renderizan datos
```

---

## 🛠️ Stack Tecnológico

| Tecnología          | Versión | Propósito               |
| ------------------- | ------- | ----------------------- |
| **React**           | 18.2.0  | Biblioteca UI           |
| **TypeScript**      | 5.2.2   | Type safety             |
| **Vite**            | 5.0.8   | Build tool y dev server |
| **React Router**    | 6.20.0  | Enrutamiento            |
| **Axios**           | 1.6.2   | Cliente HTTP            |
| **React Hook Form** | 7.48.2  | Manejo de formularios   |
| **Zod**             | 3.22.4  | Validación de esquemas  |
| **Tailwind CSS**    | 3.3.6   | Estilos                 |
| **Nginx**           | Alpine  | Servidor de producción  |

---

## 📁 Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   └── AuthGuard.tsx    # Guard de autenticación
│   ├── config/              # Configuración
│   │   └── api.ts           # Endpoints y URLs base
│   ├── contexts/            # Context API de React
│   │   └── AuthContext.tsx  # Estado global de autenticación
│   ├── pages/               # Páginas/views
│   │   ├── LoginPage.tsx
│   │   ├── ProductsPage.tsx
│   │   └── ProductFormPage.tsx
│   ├── routes/              # Configuración de rutas
│   │   └── AppRouter.tsx    # Router modular
│   ├── services/            # Servicios de API
│   │   └── api.ts           # Cliente HTTP con interceptores
│   ├── types/               # Definiciones TypeScript
│   │   └── index.ts         # Interfaces y tipos
│   ├── utils/               # Utilidades
│   │   └── storage.ts       # Manejo de localStorage
│   ├── App.tsx              # Componente raíz
│   ├── App.css              # Estilos globales
│   └── main.tsx             # Punto de entrada
├── Dockerfile               # Imagen de producción
├── nginx.conf              # Configuración Nginx
├── package.json            # Dependencias
├── tsconfig.json           # Configuración TypeScript
└── vite.config.ts          # Configuración Vite
```

---

## 🔐 Autenticación y Autorización

### Flujo de Autenticación

1. **Login (`LoginPage.tsx`)**

   - Usuario ingresa username y password
   - Se valida con `react-hook-form` y `zod`
   - Se llama a `apiService.login()` que hace POST a `/auth/token`
   - El endpoint retorna `{ access_token, token_type }`
   - El token se guarda en `localStorage` mediante `storage.setToken()`

2. **Almacenamiento del Token**

   ```typescript
   // utils/storage.ts
   localStorage.setItem("asisya_token", token);
   ```

3. **Interceptor HTTP (`services/api.ts`)**

   - **Request Interceptor**: Agrega automáticamente el header `Authorization: Bearer {token}` a cada request
   - **Response Interceptor**: Si recibe 401, elimina el token y redirige a `/login`

4. **AuthGuard (`components/AuthGuard.tsx`)**
   - Componente que envuelve rutas protegidas
   - Verifica `isAuthenticated` del contexto
   - Si no está autenticado, redirige a `/login` preservando la ruta original

### Código Clave

```typescript
// Request Interceptor
this.client.interceptors.request.use((config) => {
  const token = storage.getToken();
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response Interceptor
this.client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      storage.removeToken();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
```

---

## 🌐 Comunicación con la API

### Cliente HTTP Centralizado

El servicio `apiService` (`services/api.ts`) es un singleton que:

- Configura Axios con `baseURL` desde variables de entorno
- Implementa interceptores para tokens y errores
- Expone métodos tipados para cada endpoint

### Endpoints Utilizados

| Método | Endpoint      | Descripción                          |
| ------ | ------------- | ------------------------------------ |
| `POST` | `/auth/token` | Login (OAuth2 form-data)             |
| `GET`  | `/products`   | Listar productos (paginado, filtros) |
| `POST` | `/products`   | Crear producto (multipart/form-data) |
| `GET`  | `/categories` | Listar categorías                    |

### Ejemplo de Uso

```typescript
// Obtener productos con filtros
const products = await apiService.getProducts({
  page: 1,
  per_page: 10,
  name: "silla",
  available: true,
  min_price: 100,
  max_price: 500,
});

// Crear producto
const newProduct = await apiService.createProduct({
  name: "Producto",
  sku: "SKU-001",
  price: 199.99,
  units_in_stock: 10,
  picture: file,
});
```

---

## 🗺️ Enrutamiento

### Router Modular (`routes/AppRouter.tsx`)

Utiliza **React Router v6** con rutas protegidas mediante `AuthGuard`:

```typescript
<Routes>
  <Route path="/login" element={<LoginPage />} />
  <Route
    path="/products"
    element={
      <AuthGuard>
        <ProductsPage />
      </AuthGuard>
    }
  />
  <Route
    path="/products/new"
    element={
      <AuthGuard>
        <ProductFormPage />
      </AuthGuard>
    }
  />
  <Route
    path="/products/:id/edit"
    element={
      <AuthGuard>
        <ProductFormPage />
      </AuthGuard>
    }
  />
</Routes>
```

### Rutas Públicas vs Protegidas

- **Pública**: `/login`
- **Protegidas**: Todas las demás (requieren autenticación)

---

## 📝 Formularios y Validación

### React Hook Form + Zod

Todos los formularios usan `react-hook-form` con validación mediante `zod`:

1. **Definición del Schema** (validación)

```typescript
const productSchema = z.object({
  name: z.string().min(1, "El nombre es requerido"),
  sku: z.string().min(1, "El SKU es requerido"),
  price: z.number().positive("El precio debe ser mayor a 0"),
  // ...
});
```

2. **Integración con React Hook Form**

```typescript
const {
  register,
  handleSubmit,
  formState: { errors },
} = useForm({
  resolver: zodResolver(productSchema),
});
```

3. **Renderizado del Formulario**

```typescript
<form onSubmit={handleSubmit(onSubmit)}>
  <input {...register("name")} />
  {errors.name && <p>{errors.name.message}</p>}
</form>
```

### Ventajas

- **Validación en cliente** antes de enviar al servidor
- **Type safety** con TypeScript
- **Mensajes de error** automáticos
- **Performance**: re-renders mínimos

---

## 🗄️ Gestión de Estado

### Context API para Autenticación

El estado de autenticación se maneja con **React Context** (`contexts/AuthContext.tsx`):

```typescript
interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}
```

### Estado Local para Datos

- **Productos**: Estado local en `ProductsPage` con `useState`
- **Formularios**: Estado manejado por `react-hook-form`
- **No se usa Redux/Zustand**: La aplicación es simple y no requiere estado global complejo

---

## 🎯 Puntos Clave para la Entrevista

### 1. **Type Safety**

- **TypeScript estricto**: `strict: true` en `tsconfig.json`
- **Interfaces para todos los tipos**: Product, Category, TokenResponse, etc.
- **No se usa `any`**: Siempre tipos explícitos

### 2. **Seguridad**

- **Token en localStorage**: Persistencia entre sesiones
- **Interceptor automático**: No hay que recordar agregar el token manualmente
- **AuthGuard**: Protección a nivel de ruta
- **Validación de formularios**: Previene datos inválidos

### 3. **Arquitectura Limpia**

- **Separación de responsabilidades**: servicios, componentes, páginas
- **Reutilización**: Componentes y hooks compartidos
- **Mantenibilidad**: Código modular y fácil de extender

### 4. **Performance**

- **Code splitting**: Vite lo hace automáticamente
- **Lazy loading**: Posible con `React.lazy()` si se necesita
- **Optimizaciones de React**: `useMemo`, `useCallback` cuando sea necesario

### 5. **UX/UI**

- **Feedback visual**: Loading states, errores, mensajes de éxito
- **Accesibilidad**: Labels, aria-attributes, semantic HTML
- **Responsive**: Tailwind CSS para diseño adaptable

### 6. **Integración con Backend**

- **Formato correcto**: OAuth2 form-data para login, multipart/form-data para productos
- **Manejo de errores**: Interceptores capturan 401, 400, 500, etc.
- **Tipos sincronizados**: Interfaces TypeScript coinciden con DTOs del backend

---

## 🐳 Docker y Despliegue

### Dockerfile Multi-stage

1. **Build stage**: Compila la aplicación con Node.js
2. **Production stage**: Sirve archivos estáticos con Nginx

### Nginx Configuration

- **SPA fallback**: Todas las rutas van a `index.html`
- **Cache de assets**: JS/CSS con expiración de 1 año
- **Proxy API**: Opcional para desarrollo (en producción, CORS desde backend)

---

## 🔧 Comandos Principales

```bash
# Desarrollo
npm run dev          # Inicia Vite dev server (puerto 3000)

# Producción
npm run build        # Compila para producción
npm run preview      # Preview de la build

# Linting
npm run lint         # Ejecuta ESLint
```

---

## 📌 Notas Importantes

1. **Variables de Entorno**: `VITE_API_BASE_URL` debe apuntar al backend
2. **CORS**: El backend debe permitir requests desde el frontend
3. **Token Expiration**: Actualmente no se maneja expiración automática (se puede agregar)
4. **Error Handling**: Errores se muestran en UI, pero se pueden mejorar con toast notifications
5. **API Compatibility**: El frontend envía datos según `ProductCreateDTO` (name, sku, description, quantity_per_unit, units_in_stock, units_on_order, discontinued, price, available, category_id). Si el controlador del backend espera campos diferentes (slug, stock), puede haber un error 400. Esto requeriría ajustar el backend para que coincida con el DTO.

---

## 🚀 Mejoras Futuras Sugeridas

1. **Refresh Token**: Implementar refresh automático antes de expiración
2. **Toast Notifications**: Librería como `react-toastify` para feedback
3. **Loading Skeletons**: Mejor UX durante carga
4. **Optimistic Updates**: Actualizar UI antes de confirmación del servidor
5. **Tests**: Unit tests con Vitest, E2E con Playwright

---

## 📞 Preguntas Frecuentes para la Entrevista

**P: ¿Por qué usar Context API en lugar de Redux?**
R: La aplicación es simple, no requiere estado global complejo. Context API es suficiente y reduce overhead.

**P: ¿Cómo se maneja la expiración del token?**
R: Actualmente, si el token expira, el interceptor detecta el 401 y redirige a login. Se puede mejorar con refresh tokens.

**P: ¿Por qué React Hook Form en lugar de formularios controlados?**
R: Mejor performance (menos re-renders), validación integrada, menos código boilerplate.

**P: ¿Cómo se asegura la seguridad del token?**
R: Se guarda en localStorage (persistencia), pero en producción se podría considerar httpOnly cookies para mayor seguridad.

---

**Última actualización**: Diciembre 2024
