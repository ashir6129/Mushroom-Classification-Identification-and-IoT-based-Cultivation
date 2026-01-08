# Sanity CMS Setup for Portfolio

This directory contains the Sanity CMS schema for managing project images.

## Setup Instructions

1. Create a Sanity account at [sanity.io](https://sanity.io)
2. Create a new project
3. Add your project details to `.env.local`:
   ```
   NEXT_PUBLIC_SANITY_PROJECT_ID=your_project_id
   NEXT_PUBLIC_SANITY_DATASET=production
   ```

## Schema

The `project` schema allows you to:
- Match projects by GitHub repo name
- Override title and description
- Upload multiple images
- Mark projects as featured

## Project Schema Fields

| Field | Type | Description |
|-------|------|-------------|
| repoName | string | Must match GitHub repo name exactly |
| title | string | Optional display title override |
| description | text | Optional description override |
| images | array of images | Project screenshots/gallery |
| featured | boolean | Show in featured section |
