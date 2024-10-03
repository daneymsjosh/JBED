<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ContactController;

Route::post('/upload', [ContactController::class, 'upload']);

Route::apiResource('contacts', ContactController::class)->except('create');
