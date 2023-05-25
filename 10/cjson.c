#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

static PyObject* cjson_loads(PyObject* self, PyObject* args)
{
    bool valid = false;
    const char* json;
    if (!PyArg_ParseTuple(args, "s", &json))
    {
        PyErr_Format(PyExc_TypeError, "Expected string input");
        return NULL;
    }

    if (json[0] == '\0')
    {
        PyErr_Format(PyExc_TypeError, "Empty JSON string");
        return NULL;
    }

    if (json[0] != '{')
    {
        PyErr_Format(PyExc_TypeError, "Expected object");
        return NULL;
    }

    PyObject* dict = PyDict_New();

    if (!dict)
    {
        PyErr_Format(PyExc_MemoryError, "Failed to create dict object");
        return NULL;
    }

    json++;

    while (*json != '\0')
    {
        if (*json == '}')
        {
            json++;
            if (*json != '\0')
            {
                PyErr_Format(PyExc_TypeError, "Invalid JSON string");
                Py_DECREF(dict);
                return NULL;
            }
            else
            {
                valid = true;
                continue;
            }
        }

        while (*json == ' ')
        {
            json++;
        }

        if (*json != '\"')
        {
            PyErr_Format(PyExc_TypeError, "Expected object key");
            Py_DECREF(dict);
            return NULL;
        }

        json++;

        const char* key_start = json;
        while (*json != '\"')
        {
            if (*json == '\0')
            {
                PyErr_Format(PyExc_TypeError, "Expected closing '\"' for object key");
                Py_DECREF(dict);
                return NULL;
            }
            json++;
        }

        PyObject* key = PyUnicode_FromStringAndSize(key_start, json - key_start);
        if (!key)
        {
            PyErr_Format(PyExc_MemoryError, "Failed to create string object");
            Py_DECREF(dict);
            return NULL;
        }

        json++;

        while (*json == ' ')
        {
            json++;
        }

        if (*json != ':')
        {
            PyErr_Format(PyExc_TypeError, "Expected ':' after object key");
            Py_DECREF(key);
            Py_DECREF(dict);
            return NULL;
        }

        json++;

        while (*json == ' ')
        {
            json++;
        }

        if (*json == '\0' || *json == '}')
        {
            PyErr_Format(PyExc_TypeError, "Expected value after ':'");
            Py_DECREF(key);
            Py_DECREF(dict);
            return NULL;
        }

        PyObject* value = NULL;

        if (*json == '\"')
        {
            json++;

            const char* value_start = json;
            while (*json != '\"')
            {
                if (*json == '\0')
                {
                    PyErr_Format(PyExc_TypeError, "Expected closing '\"' for string value");
                    Py_DECREF(key);
                    Py_DECREF(dict);
                    return NULL;
                }
                json++;
            }

            value = PyUnicode_FromStringAndSize(value_start, json - value_start);
            if (!value)
            {
                PyErr_Format(PyExc_MemoryError, "Failed to create string object");
                Py_DECREF(key);
                Py_DECREF(dict);
                return NULL;
            }

            json++;
        }
        else
        {
            char* endptr;
            double num = strtod(json, &endptr);

            if (endptr == json)
            {
                PyErr_Format(PyExc_TypeError, "Expected number value");
                Py_DECREF(key);
                Py_DECREF(dict);
                return NULL;
            }

            value = PyFloat_FromDouble(num);
            if (!value)
            {
                PyErr_Format(PyExc_MemoryError, "Failed to create number object");
                Py_DECREF(key);
                Py_DECREF(dict);
                return NULL;
            }

            json = endptr;
        }

        if (PyDict_SetItem(dict, key, value) < 0)
        {
            PyErr_Format(PyExc_RuntimeError, "Failed to set item in dictionary");
            Py_DECREF(key);
            Py_DECREF(value);
            Py_DECREF(dict);
            return NULL;
        }

        Py_DECREF(key);
        Py_DECREF(value);

        while (*json == ' ')
        {
            json++;
        }

        if (*json != ',' && *json != '}')
        {
            PyErr_Format(PyExc_TypeError, "Expected ',' after key and value pair");
            Py_DECREF(dict);
            return NULL;
        }

        if (*json == ',')
        {
            json++;
        }

        while (*json == ' ')
        {
            json++;
        }
    }

    if (valid == false)
    {
        PyErr_Format(PyExc_TypeError, "Invalid JSON string");
        return NULL;
    }

    return dict;
}

static PyObject* cjson_dumps(PyObject* self, PyObject* args)
{
    PyObject* dict;
    if (!PyArg_ParseTuple(args, "O", &dict))
    {
        PyErr_Format(PyExc_TypeError, "Expected dictionary object");
        return NULL;
    }

    if (!PyDict_Check(dict))
    {
        PyErr_Format(PyExc_TypeError, "Expected dictionary object");
        return NULL;
    }

    PyObject* items = PyDict_Items(dict);
    if (!items)
    {
        PyErr_Format(PyExc_MemoryError, "Failed to get dictionary items");
        return NULL;
    }

    Py_ssize_t size = PyList_Size(items);
    if (size == -1)
    {
        Py_DECREF(items);
        PyErr_Format(PyExc_MemoryError, "Failed to get list size");
        return NULL;
    }

    char* json = (char*)malloc(3);
    if (!json)
    {
        Py_DECREF(items);
        PyErr_Format(PyExc_MemoryError, "Failed to allocate memory for JSON string");
        return NULL;
    }

    json[0] = '{';
    json[1] = '\0';

    Py_ssize_t json_index = 1;

    bool is_num;

    for (Py_ssize_t i = 0; i < size; i++)
    {
        PyObject* item = PyList_GetItem(items, i);
        PyObject* key = PyTuple_GetItem(item, 0);
        PyObject* value = PyTuple_GetItem(item, 1);

        if (!PyUnicode_Check(key))
        {
            Py_DECREF(items);
            free(json);
            PyErr_Format(PyExc_TypeError, "Dictionary keys must be strings");
            return NULL;
        }

        if (!PyUnicode_Check(value) && !PyFloat_Check(value) && !PyLong_Check(value))
        {
            Py_DECREF(items);
            free(json);
            PyErr_Format(PyExc_TypeError, "Dictionary values must be strings or numbers");
            return NULL;
        }

        const char* key_str = PyUnicode_AsUTF8(key);
        const char* value_str;

        if (PyUnicode_Check(value))
        {
            is_num = false;
            value_str = PyUnicode_AsUTF8(value);
        }
        else
        {
            is_num = true;
            value_str = PyOS_double_to_string(PyFloat_AsDouble(value), 'g', 17, 0, NULL);
        }

        json = (char*)realloc(json, strlen(json) + strlen(key_str) + 4 + strlen(value_str) + 4);

        json[json_index++] = '"';
        strcpy(json + json_index, key_str);
        json_index += strlen(key_str);
        json[json_index++] = '"';
        json[json_index++] = ':';
        json[json_index++] = ' ';
        if (is_num == false)
        {
            json[json_index++] = '"';
        }
        strcpy(json + json_index, value_str);
        json_index += strlen(value_str);
        if (is_num == false)
        {
            json[json_index++] = '"';
        }

        if (i < size - 1)
        {
            json[json_index++] = ',';
            json[json_index++] = ' ';
        }
    }

    json[json_index++] = '}';
    json[json_index] = '\0';

    Py_DECREF(items);

    PyObject* result = PyUnicode_FromString(json);
    free(json);

    return result;
}

static PyMethodDef cjson_methods[] =
{
    {"loads", cjson_loads, METH_VARARGS, "Parse JSON string and return dictionary object"},
    {"dumps", cjson_dumps, METH_VARARGS, "Serialize dictionary object to JSON string"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cjson_module =
{
    PyModuleDef_HEAD_INIT,
    "cjson",
    "JSON parsing and serialization module",
    -1,
    cjson_methods
};

PyMODINIT_FUNC PyInit_cjson(void)
{
    return PyModule_Create(&cjson_module);
}