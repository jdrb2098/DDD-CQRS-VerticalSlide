import { Routes, Route, Navigate } from "react-router-dom";
import { AuthGuard } from "@/components/AuthGuard";
import { Layout } from "@/components/Layout";
import { LoginPage } from "@/pages/LoginPage";
import { ProductsPage } from "@/pages/ProductsPage";
import { ProductFormPage } from "@/pages/ProductFormPage";
import { CategoriesPage } from "@/pages/CategoriesPage";
import { CategoryFormPage } from "@/pages/CategoryFormPage";

export function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/products"
        element={
          <AuthGuard>
            <Layout>
              <ProductsPage />
            </Layout>
          </AuthGuard>
        }
      />
      <Route
        path="/products/new"
        element={
          <AuthGuard>
            <Layout>
              <ProductFormPage />
            </Layout>
          </AuthGuard>
        }
      />
      <Route
        path="/products/:id/edit"
        element={
          <AuthGuard>
            <Layout>
              <ProductFormPage />
            </Layout>
          </AuthGuard>
        }
      />
      <Route
        path="/categories"
        element={
          <AuthGuard>
            <Layout>
              <CategoriesPage />
            </Layout>
          </AuthGuard>
        }
      />
      <Route
        path="/categories/new"
        element={
          <AuthGuard>
            <Layout>
              <CategoryFormPage />
            </Layout>
          </AuthGuard>
        }
      />
      <Route path="/" element={<Navigate to="/products" replace />} />
      <Route path="*" element={<Navigate to="/products" replace />} />
    </Routes>
  );
}
