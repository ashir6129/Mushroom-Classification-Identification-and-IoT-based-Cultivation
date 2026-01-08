// Sanity Project Schema
// Use this schema when setting up your Sanity project

export default {
    name: "project",
    title: "Project",
    type: "document",
    fields: [
        {
            name: "repoName",
            title: "GitHub Repository Name",
            type: "string",
            description: "Must match the exact GitHub repository name (e.g., 'my-awesome-project')",
            validation: (Rule: any) => Rule.required(),
        },
        {
            name: "title",
            title: "Display Title",
            type: "string",
            description: "Optional: Override the display title (defaults to repo name)",
        },
        {
            name: "description",
            title: "Description",
            type: "text",
            rows: 3,
            description: "Optional: Override the project description",
        },
        {
            name: "images",
            title: "Project Images",
            type: "array",
            of: [
                {
                    type: "image",
                    options: {
                        hotspot: true,
                    },
                    fields: [
                        {
                            name: "alt",
                            title: "Alt Text",
                            type: "string",
                        },
                    ],
                },
            ],
            description: "Upload screenshots and images for this project",
        },
        {
            name: "featured",
            title: "Featured Project",
            type: "boolean",
            description: "Show this project in the featured section on the home page",
            initialValue: false,
        },
    ],
    preview: {
        select: {
            title: "title",
            repoName: "repoName",
            media: "images.0",
        },
        prepare({ title, repoName, media }: any) {
            return {
                title: title || repoName,
                subtitle: repoName,
                media,
            };
        },
    },
};
