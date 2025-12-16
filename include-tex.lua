function CodeBlock(cb)
  if cb.classes:includes("include-tex") then
    local filename = cb.attributes["file"]
    local f = io.open(filename, "r")
    if not f then
      return cb
    end
    local content = f:read("*all")
    f:close()
    return pandoc.CodeBlock(content, { "tex" })
  end
end
