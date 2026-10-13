<?php

use function Pest\Laravel\getJson;

it('reports that the API is up', function () {
    getJson('/api/health')
        ->assertOk()
        ->assertExactJson(['status' => 'ok']);
});

it('does not serve routes outside /api', function () {
    getJson('/health')->assertNotFound();
});
