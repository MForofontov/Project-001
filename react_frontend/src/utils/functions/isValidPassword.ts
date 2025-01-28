const isValidPassword = (password: string): boolean => {
    const criteria = [
      { text: 'At least 8 characters', test: (pw: string) => pw.length >= 8 },
      { text: 'At least one uppercase letter', test: (pw: string) => /[A-Z]/.test(pw) },
      { text: 'At least one lowercase letter', test: (pw: string) => /[a-z]/.test(pw) },
      { text: 'At least one number', test: (pw: string) => /\d/.test(pw) },
      { text: 'At least one special character', test: (pw: string) => /[!@#$%^&*(),.?":{}|<>]/.test(pw) },
    ];
  
    return criteria.every(criterion => criterion.test(password));
};
  
export default isValidPassword;