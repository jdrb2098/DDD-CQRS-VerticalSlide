import { apiService } from "@/services/api";
import { Category, ProductCreateRequest } from "@/types";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { z } from "zod";

const productSchema = z.object({
  name: z
    .string()
    .min(1, "El nombre es requerido")
    .max(200, "El nombre es demasiado largo"),
  sku: z.string().max(100, "El sku es demasiado largo"),
  description: z
    .string()
    .max(1000, "La descripción es demasiado larga")
    .optional()
    .or(z.literal("")),
  price: z.number().positive("El precio debe ser mayor a 0"),
  stock: z.number().int().min(0, "El stock no puede ser negativo"),
  category_id: z.number().int().positive().optional().or(z.literal("")),
  picture: z.instanceof(File).optional(),
});

type ProductFormData = z.infer<typeof productSchema>;

export function ProductFormPage() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const isEdit = !!id;
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoadingCategories, setIsLoadingCategories] = useState<boolean>(true);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProductFormData>({
    resolver: zodResolver(productSchema),
    defaultValues: {
      stock: 0, // Valor por defecto para stock
    },
  });

  useEffect(() => {
    loadCategories();
    if (isEdit) {
      // Note: Update endpoint not implemented in API yet, so edit mode is limited
      // This would load existing product data if update endpoint exists
    }
  }, [isEdit, id]);

  const loadCategories = async (): Promise<void> => {
    try {
      const data = await apiService.getCategories();
      setCategories(data);
    } catch (err) {
      console.error("Error loading categories:", err);
    } finally {
      setIsLoadingCategories(false);
    }
  };

  const onSubmit = async (data: ProductFormData): Promise<void> => {
    setError(null);
    setIsSubmitting(true);

    try {
      const productData: ProductCreateRequest = {
        name: data.name,
        sku: data.sku,
        description: data.description || undefined,
        price: data.price,
        stock: data.stock, // Requerido por el controlador
        category_id:
          data.category_id !== undefined
            ? typeof data.category_id === "string" && data.category_id !== ""
              ? Number(data.category_id)
              : typeof data.category_id === "number"
              ? data.category_id
              : undefined
            : undefined,
      };

      if (isEdit) {
        // Update endpoint not available in API yet
        setError("La funcionalidad de edición aún no está disponible");
        return;
      } else {
        await apiService.createProduct(productData);
        navigate("/products", { replace: true });
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Error al guardar el producto";
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">
        {isEdit ? "Editar Producto" : "Crear Producto"}
      </h1>

      {error && (
        <div
          className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded"
          role="alert"
        >
          {error}
        </div>
      )}

      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white rounded-lg shadow-md p-6 space-y-6"
      >
        <div>
          <label
            htmlFor="name"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Nombre <span className="text-red-500">*</span>
          </label>
          <input
            id="name"
            type="text"
            {...register("name")}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            aria-invalid={errors.name ? "true" : "false"}
            aria-describedby={errors.name ? "name-error" : undefined}
          />
          {errors.name && (
            <p
              id="name-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.name.message}
            </p>
          )}
        </div>

        <div>
          <label
            htmlFor="sku"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            SKU <span className="text-red-500">*</span>
          </label>
          <input
            id="sku"
            type="text"
            {...register("sku")}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            aria-invalid={errors.sku ? "true" : "false"}
            aria-describedby={errors.sku ? "sku-error" : undefined}
            placeholder="producto-ejemplo"
          />
          {errors.sku && (
            <p
              id="sku-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.sku.message}
            </p>
          )}
        </div>

        <div>
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Descripción
          </label>
          <textarea
            id="description"
            {...register("description")}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            aria-invalid={errors.description ? "true" : "false"}
            aria-describedby={
              errors.description ? "description-error" : undefined
            }
          />
          {errors.description && (
            <p
              id="description-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label
              htmlFor="price"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Precio <span className="text-red-500">*</span>
            </label>
            <input
              id="price"
              type="number"
              step="0.01"
              min="0.01"
              {...register("price", { valueAsNumber: true })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              aria-invalid={errors.price ? "true" : "false"}
              aria-describedby={errors.price ? "price-error" : undefined}
            />
            {errors.price && (
              <p
                id="price-error"
                className="mt-1 text-sm text-red-600"
                role="alert"
              >
                {errors.price.message}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="stock"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Stock <span className="text-red-500">*</span>
            </label>
            <input
              id="stock"
              type="number"
              min="0"
              {...register("stock", { valueAsNumber: true })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              aria-invalid={errors.stock ? "true" : "false"}
              aria-describedby={errors.stock ? "stock-error" : undefined}
            />
            {errors.stock && (
              <p
                id="stock-error"
                className="mt-1 text-sm text-red-600"
                role="alert"
              >
                {errors.stock.message}
              </p>
            )}
          </div>
        </div>

        <div>
          <label
            htmlFor="category_id"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Categoría
          </label>
          {isLoadingCategories ? (
            <div className="text-sm text-gray-500">Cargando categorías...</div>
          ) : (
            <select
              id="category_id"
              {...register("category_id", {
                setValueAs: (value) =>
                  value === "" ? undefined : Number(value),
              })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Sin categoría</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          )}
        </div>

        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate("/products")}
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? "Guardando..." : isEdit ? "Actualizar" : "Crear"}
          </button>
        </div>
      </form>
    </div>
  );
}
