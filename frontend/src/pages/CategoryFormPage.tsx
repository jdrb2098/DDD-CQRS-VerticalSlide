import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { apiService } from "@/services/api";
import { CategoryCreateRequest } from "@/types";

const categorySchema = z.object({
  name: z
    .string()
    .min(1, "El nombre es requerido")
    .max(200, "El nombre es demasiado largo"),
  slug: z
    .string()
    .max(100, "El slug es demasiado largo")
    .optional()
    .or(z.literal("")),
  description: z
    .string()
    .max(1000, "La descripción es demasiado larga")
    .optional()
    .or(z.literal("")),
  picture: z.instanceof(File).optional(),
});

type CategoryFormData = z.infer<typeof categorySchema>;

export function CategoryFormPage() {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [pictureFile, setPictureFile] = useState<File | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm<CategoryFormData>({
    resolver: zodResolver(categorySchema),
  });

  const onSubmit = async (data: CategoryFormData): Promise<void> => {
    setError(null);
    setIsSubmitting(true);

    try {
      const categoryData: CategoryCreateRequest = {
        name: data.name,
        slug: data.slug || undefined,
        description: data.description || undefined,
        picture: pictureFile || undefined,
      };

      await apiService.createCategory(categoryData);
      navigate("/categories", { replace: true });
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Error al guardar la categoría";
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Crear Categoría</h1>

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
            htmlFor="slug"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Slug
          </label>
          <input
            id="slug"
            type="text"
            {...register("slug")}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            aria-invalid={errors.slug ? "true" : "false"}
            aria-describedby={errors.slug ? "slug-error" : undefined}
            placeholder="categoria-ejemplo"
          />
          {errors.slug && (
            <p
              id="slug-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.slug.message}
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

        <div>
          <label
            htmlFor="picture"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Imagen
          </label>
          <input
            id="picture"
            type="file"
            accept="image/*"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) {
                setPictureFile(file);
                setValue("picture", file);
              }
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          {pictureFile && (
            <p className="mt-1 text-sm text-gray-500">
              Archivo seleccionado: {pictureFile.name}
            </p>
          )}
        </div>

        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate("/categories")}
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? "Guardando..." : "Crear"}
          </button>
        </div>
      </form>
    </div>
  );
}
