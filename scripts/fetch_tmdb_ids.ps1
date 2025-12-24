param(
    [Parameter(Mandatory=$true)][int]$companyId,
    [Parameter(Mandatory=$false)][string]$studio = 'studio',
    [Parameter(Mandatory=$false)][string]$out = "data/raw/tmdb_studio.json"
)

if (-not $env:TMDB_API_KEY) {
    Write-Error "TMDB_API_KEY not set. Put it in the environment or .env"
    exit 1
}

python .\src\tmdb\get_studio_movies.py --company-id $companyId --studio $studio --out $out
