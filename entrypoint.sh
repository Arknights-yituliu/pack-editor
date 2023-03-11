#!/bin/bash

gunicorn pack_editor.wsgi -b 0.0.0.0:9000
