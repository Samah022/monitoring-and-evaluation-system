import * as Yup from 'yup';

const cameraSchema = Yup.object().shape({
    name: Yup.string()
        .trim()
        .required('*Name should not be empty.')
        .matches(/^[a-zA-Z0-9\s()-]*$/, {
            message: '*Camera name can only contain letters, numbers, and hyphens.',
            excludeEmptyString: true,
        })
        .max(50, '*Camera name should be less than 50 characters.'),
    link: Yup.string()
        .trim()
        .required('*Camera link should not be empty.')
        .matches(/^rtsp:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\/[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+$/, {
            message: '*Invalid camera link format.',
            excludeEmptyString: true,
        })
        .max(50, '*Camera link should be less than 50 characters.'),
});

export async function validateCameraObject(values) {
    try {
        await cameraSchema.validate(values, { abortEarly: false });
        return {};

    } catch (validationError) {
        const error = {};
        validationError.inner.forEach((err) => {
            error[err.path] = err.message;
        });
        return error;
    }
}

