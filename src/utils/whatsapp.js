/**
 * Generates a WhatsApp link with a pre-filled message.
 * @param {string} productName - The name of the product.
 * @param {string} [brandName] - The brand of the product (optional).
 * @param {string} [categoryName] - The category of the product (optional).
 * @returns {string} The fully formed WhatsApp URL.
 */
export function generateWhatsAppLink(productName, brandName = '', categoryName = '') {
    const phoneNumber = "59169453151";

    let message = `Hola Mishkila! Me interesa: ${productName}`;

    if (brandName) {
        message += ` de ${brandName}`;
    }

    if (categoryName) {
        message += ` - ${categoryName}`;
    }

    message += `. ¿Precio y disponibilidad?`;

    const encodedMessage = encodeURIComponent(message);
    return `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
}
