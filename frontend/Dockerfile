# Stage 1: Build the Angular application
FROM node:16 as build

WORKDIR /app

ARG configuration=production
ARG base_href=/


# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build -- --configuration=${configuration} --base-href=${base_href}

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Copy the build output to replace the default nginx contents
COPY --from=build /app/dist/newts /usr/share/nginx/html

# Copy custom nginx configuration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf


# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
