<?php

use App\Http\Controllers\HealthController;
use Illuminate\Support\Facades\Route;

// Every route in this file gets the "/api" prefix and the stateless "api" middleware group (bootstrap/app.php).
Route::get('/health', HealthController::class);
