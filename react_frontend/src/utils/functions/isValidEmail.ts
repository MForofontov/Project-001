/**
 * Checks if a string is a valid email address.
 * 
 * @param email - The string to check.
 * @returns True if the string is a valid email address, false otherwise.
 */
function isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
}

export default isValidEmail;