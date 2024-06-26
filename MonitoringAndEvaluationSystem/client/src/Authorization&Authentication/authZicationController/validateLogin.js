import * as Yup from 'yup';

const loginSchema = Yup.object().shape({
    email: Yup.string()
        .trim()
        .required('*Email address is required.')
        .email('*Invalid email address.'),
    password: Yup.string()
        .trim()
        .required('*Password is required.'),
});

export async function validateLogin(values) {
    try {
        await loginSchema.validate(values, { abortEarly: false });
        return {};
    } catch (validationError) {
        const errors = {};
        validationError.inner.forEach((err) => {
            errors[err.path] = err.message;
        });
        return errors;
    }
}