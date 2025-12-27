import type { ImageMetadata } from 'astro';

const images = import.meta.glob<{ default: ImageMetadata }>('/src/assets/images/**/*.{jpeg,jpg,png,gif}');

export async function resolveImage(imagePath: string): Promise<ImageMetadata | string> {
    // If it's already an external URL (like Unsplash), return it as is
    if (imagePath.startsWith('http')) {
        return imagePath;
    }

    // Normalize path: replace /images/ with /src/assets/images/
    // The data has paths like: /images/products/parati/...
    // We want to match keys like: /src/assets/images/products/parati/...

    let key = imagePath;
    if (imagePath.startsWith('/images/')) {
        key = imagePath.replace('/images/', '/src/assets/images/');
    } else if (!imagePath.startsWith('/src/assets/')) {
        // fallback if path didn't start with /images
        key = `/src/assets/images${imagePath.startsWith('/') ? '' : '/'}${imagePath}`;
    }

    const loader = images[key];

    if (!loader) {
        console.error(`Image not found for path: ${imagePath} (key: ${key})`);
        // Return the original path as a fallback string so it might at least try to load (though it will likely 404 if moved)
        return imagePath;
    }

    const mod = await loader();
    return mod.default;
}
