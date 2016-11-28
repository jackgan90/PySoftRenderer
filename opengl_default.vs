#version 430

layout(location = 0)in vec4 position;
layout(location = 1)in vec4 texcoord;

out vec4 uv;

void main()
{
	uv = texcoord;
	gl_Position = position;
}

