<?php

use Tests\TestCase;

/*
|--------------------------------------------------------------------------
| Test Case
|--------------------------------------------------------------------------
|
| Feature tests boot the Laravel application, so they can send requests to the API
| with helpers such as getJson(). Unit tests run plain PHP, without the framework.
|
*/

pest()->extend(TestCase::class)->in('Feature');
